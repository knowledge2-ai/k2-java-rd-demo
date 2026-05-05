#!/usr/bin/env python3
"""Run patch-generation tasks and compare final code output, time, and tokens."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from k2_java_rd_demo.codex_comparison import CodexCliConfig, run_codex_answer  # noqa: E402
from k2_java_rd_demo.assets import generate_seed_guides  # noqa: E402
from k2_java_rd_demo.k2_mcp_server import (  # noqa: E402
    HYBRID_PROFILES,
    PROJECT_ID,
    K2McpConfig,
    K2McpServer,
)
from k2_java_rd_demo.patch_benchmark import (  # noqa: E402
    PATCH_ARM_NAMES,
    PatchTask,
    VerificationCommand,
    classify_codex_infra_failure,
    extract_changed_files,
    extract_codex_usage_metrics,
    patch_generation_prompt,
    patch_tasks,
    render_patch_report,
    score_patch_run,
    summarize_patch_scorecard,
    validate_local_java_imports,
)

MCP_SERVER = ROOT / "scripts" / "k2_java_rd_mcp_server.py"
DEFAULT_SOURCE_BASE = Path("/tmp/k2-java-rd-demo-sources")
DEFAULT_ARMS = ("codex_repo_plus_guides_dump", "codex_with_k2_mcp")
LOCAL_AGENT_FEATURES = (
    "features.browser_use=false",
    "features.web_search_request=false",
)
DIFF_PATHSPEC = (
    ".",
    ":(exclude)**/target/**",
    ":(exclude)**/build/**",
    ":(exclude).gradle/**",
    ":(exclude)**/.gradle/**",
    ":(exclude)**/.plxarc",
    ":(exclude)**/gradle-wrapper.jar",
)


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.env_file:
        _load_env_file(args.env_file)
    tasks = _selected_tasks(args)
    arms = tuple(dict.fromkeys(args.arm or DEFAULT_ARMS))
    if not tasks:
        raise SystemExit("no patch tasks selected")

    if args.preflight_only:
        _validate_live_requirements(args, arms)
        k2_probe = _probe_k2_sdk(args) if args.probe_k2_sdk else None
        print(
            json.dumps(
                {
                    "mode": "preflight",
                    "arms": arms,
                    "mcp_backend": args.mcp_backend,
                    "source_roots": _source_roots(args),
                    "k2_api_key_present": bool(os.environ.get("K2_API_KEY")),
                    "k2_probe": k2_probe,
                    "status": "ok",
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    if not args.execute:
        print(
            json.dumps(
                {
                    "mode": "dry-run",
                    "task_count": len(tasks),
                    "tasks": [task.to_dict() for task in tasks],
                    "arms": arms,
                    "source_roots": _source_roots(args),
                    "note": "pass --execute to run Codex and write patch artifacts",
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    _validate_live_requirements(args, arms)
    k2_probe = _probe_k2_sdk(args) if args.probe_k2_sdk else None

    run_id = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ-patch-generation")
    out_dir = (args.out_dir or ROOT / "docs" / "evaluations" / "patch-runs") / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    runs: list[dict[str, Any]] = []
    for task in tasks:
        for arm_name in arms:
            runs.append(_run_task_arm(task, arm_name=arm_name, args=args, out_dir=out_dir))
            print(
                f"[{len(runs)}/{len(tasks) * len(arms)}] completed "
                f"{task.task_id} {arm_name}",
                file=sys.stderr,
                flush=True,
            )

    payload = {
        "run_id": run_id,
        "generated_at": datetime.now(UTC).isoformat(),
        "method": "patch_generation_code_output_time_tokens",
        "model": args.model,
        "project_id": args.project_id,
        "source_roots": _source_roots(args),
        "retrieval_profile": args.retrieval_profile,
        "retrieval_profiles": HYBRID_PROFILES,
        "preflight": {
            "mcp_backend": args.mcp_backend,
            "k2_probe": k2_probe,
            "probe_k2_sdk": bool(args.probe_k2_sdk),
        },
        "run_tests": args.run_tests,
        "tasks": [task.to_dict() for task in tasks],
        "summary": summarize_patch_scorecard(runs),
        "runs": runs,
    }
    result_path = out_dir / "patch-scorecard.json"
    report_path = out_dir / "patch-report.md"
    _write_text(result_path, json.dumps(payload, indent=2, sort_keys=True))
    _write_text(report_path, render_patch_report(payload))
    print(
        json.dumps(
            {
                "result_path": str(result_path),
                "report_path": str(report_path),
                "summary": payload["summary"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def _run_task_arm(
    task: PatchTask,
    *,
    arm_name: str,
    args: argparse.Namespace,
    out_dir: Path,
) -> dict[str, Any]:
    task_dir = out_dir / "worktrees" / task.task_id / arm_name
    artifact_dir = out_dir / "artifacts" / task.task_id / arm_name
    artifact_dir.mkdir(parents=True, exist_ok=True)
    source_root = _source_root_for_task(task, args)
    _materialize_worktree(source_root, task_dir)
    if arm_name == "codex_repo_plus_guides_dump":
        _materialize_guide_dump(task, task_dir)

    prompt = patch_generation_prompt(task, arm_name=arm_name)
    _write_text(artifact_dir / "prompt.txt", prompt)
    event_path = artifact_dir / "codex-events.jsonl"
    answer_path = artifact_dir / "answer.md"

    start = time.perf_counter()
    error_text = ""
    try:
        answer = run_codex_answer(
            prompt,
            answer_path,
            _codex_config(task_dir, task, arm_name=arm_name, args=args, event_path=event_path),
            env_allow={"K2_API_KEY"} if _is_k2_arm(arm_name) else None,
        )
    except subprocess.CalledProcessError as exc:
        answer = ""
        error_text = (exc.stderr or exc.stdout or str(exc))[-4000:]
        _write_text(artifact_dir / "codex-error.txt", error_text)
    except subprocess.TimeoutExpired as exc:
        answer = ""
        error_text = f"Codex timed out after {exc.timeout}s"
        _write_text(artifact_dir / "codex-error.txt", error_text)
    duration_s = time.perf_counter() - start
    infra_failure_reason = classify_codex_infra_failure(error_text)

    diff_text = _git_diff(task_dir)
    _write_text(artifact_dir / "patch.diff", diff_text)
    verification_results = _run_verification(task, task_dir, run_tests=args.run_tests)
    _write_text(
        artifact_dir / "verification.json",
        json.dumps(verification_results, indent=2, sort_keys=True),
    )
    events_text = event_path.read_text(encoding="utf-8") if event_path.exists() else ""
    token_metrics = extract_codex_usage_metrics(events_text)
    score = score_patch_run(
        task,
        diff_text=diff_text,
        answer_text=answer,
        verification_results=verification_results,
        duration_s=duration_s,
        token_metrics=token_metrics,
    )
    if _is_k2_arm(arm_name) and int(token_metrics.get("k2_tool_failure_count") or 0):
        score["passed"] = False
        score["failure_categories"] = sorted(
            {*score.get("failure_categories", []), "k2_mcp_tool_failure"}
        )
    if infra_failure_reason:
        score["passed"] = False
        score["failure_categories"] = sorted(
            {*score.get("failure_categories", []), "codex_infra_failure"}
        )
    if not args.keep_worktrees:
        shutil.rmtree(task_dir, ignore_errors=True)
    return {
        **score,
        "arm_name": arm_name,
        "run_status": "infra_invalid" if infra_failure_reason else "completed",
        "infra_failure_reason": infra_failure_reason,
        "answer_path": _relative_artifact_path(answer_path, out_dir),
        "patch_path": _relative_artifact_path(artifact_dir / "patch.diff", out_dir),
        "verification_path": _relative_artifact_path(artifact_dir / "verification.json", out_dir),
        "events_path": _relative_artifact_path(event_path, out_dir),
        "answer_chars": len(answer),
        "error": error_text,
    }


def _codex_config(
    cwd: Path,
    task: PatchTask,
    *,
    arm_name: str,
    args: argparse.Namespace,
    event_path: Path,
) -> CodexCliConfig:
    overrides = list(LOCAL_AGENT_FEATURES)
    if _is_k2_arm(arm_name):
        overrides.extend(
            [
                f'mcp_servers.k2-java-rd.command="{MCP_SERVER}"',
                f'mcp_servers.k2-java-rd.env.K2_MCP_BACKEND="{args.mcp_backend}"',
                f'mcp_servers.k2-java-rd.env.K2_MCP_NAMESPACE="{args.namespace}"',
                f'mcp_servers.k2-java-rd.env.K2_MCP_DEPLOYMENT="{args.deployment}"',
                f'mcp_servers.k2-java-rd.env.K2_MCP_CASE_ID="{task.task_id}"',
                f'mcp_servers.k2-java-rd.env.K2_MCP_RETRIEVAL_PROFILE="{args.retrieval_profile}"',
                f'mcp_servers.k2-java-rd.env.K2_MCP_SOURCE_BASE="{args.source_base}"',
                (
                    "mcp_servers.k2-java-rd.env.K2_MCP_DISABLE_GUIDES="
                    f'"{str(arm_name == "codex_with_k2_mcp_no_guides").lower()}"'
                ),
                (
                    "mcp_servers.k2-java-rd.env.K2_MCP_DISABLE_METADATA_FILTERS="
                    f'"{str(arm_name == "codex_with_k2_mcp_filters_off").lower()}"'
                ),
                'mcp_servers.k2-java-rd.env.K2_MCP_COMPACT_TOOL_SURFACE="true"',
                'mcp_servers.k2-java-rd.env_vars=["K2_API_KEY"]',
                *_api_host_override(args.api_host),
                "mcp_servers.k2-java-rd.startup_timeout_sec=60",
                "mcp_servers.k2-java-rd.tool_timeout_sec=240",
            ]
        )
    return CodexCliConfig(
        model=args.model,
        timeout_s=args.codex_timeout_s,
        cwd=str(cwd),
        config_overrides=tuple(overrides),
        dangerously_bypass_approvals_and_sandbox=True,
        json_events_path=event_path,
    )


def _run_verification(
    task: PatchTask,
    worktree: Path,
    *,
    run_tests: bool,
) -> list[dict[str, Any]]:
    changed_files = extract_changed_files(_git_diff(worktree))
    commands = [
        VerificationCommand(
            name="git-diff-check",
            argv=("git", "diff", "--check"),
            timeout_s=120,
        )
    ]
    if run_tests:
        commands.extend(task.verification_commands)

    results = []
    for command in commands:
        argv = _resolve_verification_argv(command.argv, worktree)
        start = time.perf_counter()
        try:
            completed = subprocess.run(
                list(argv),
                cwd=worktree,
                text=True,
                capture_output=True,
                check=False,
                timeout=command.timeout_s,
            )
            returncode = completed.returncode
            stdout = completed.stdout[-4000:]
            stderr = completed.stderr[-4000:]
        except FileNotFoundError as exc:
            returncode = 127
            stdout = ""
            stderr = str(exc)
        except subprocess.TimeoutExpired as exc:
            returncode = 124
            stdout = (exc.stdout or "")[-4000:] if isinstance(exc.stdout, str) else ""
            stderr = f"timed out after {exc.timeout}s"
        results.append(
            {
                "name": command.name,
                "argv": list(argv),
                "requested_argv": list(command.argv),
                "returncode": returncode,
                "passed": returncode == 0,
                "duration_s": round(time.perf_counter() - start, 3),
                "stdout_tail": stdout,
                "stderr_tail": stderr,
            }
        )
    if not run_tests:
        results.append(validate_local_java_imports(task, worktree, changed_files))
    return results


def _resolve_verification_argv(argv: tuple[str, ...] | list[str], worktree: Path) -> tuple[str, ...]:
    if not argv:
        return argv
    if tuple(argv) == ("git", "diff", "--check"):
        return ("git", "diff", "--check", "--", *DIFF_PATHSPEC)
    executable = argv[0]
    if executable == "./mvnw" and not (worktree / "mvnw").exists() and shutil.which("mvn"):
        return ("mvn", *argv[1:])
    if executable == "./gradlew" and not (worktree / "gradlew").exists() and shutil.which("gradle"):
        return ("gradle", *argv[1:])
    return argv


def _materialize_worktree(source_root: Path, destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not source_root.exists():
        raise SystemExit(f"source root does not exist: {source_root}")
    # The local OSS checkouts used for this demo may be partial/sparse Git
    # checkouts.  Cloning from their object database can fail if objects outside
    # the sparse working tree are missing, so materialize from working-tree
    # files and create a fresh baseline commit for diff capture.
    shutil.copytree(source_root, destination, ignore=shutil.ignore_patterns(".git"))
    subprocess.run(["git", "init"], cwd=destination, check=True, capture_output=True)
    subprocess.run(["git", "add", "."], cwd=destination, check=True, capture_output=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.name=k2-demo",
            "-c",
            "user.email=k2-demo@example.com",
            "commit",
            "-m",
            "baseline",
        ],
        cwd=destination,
        check=True,
        capture_output=True,
    )


def _materialize_guide_dump(task: PatchTask, destination: Path) -> None:
    dump_root = destination / ".k2-demo-confluence-dump"
    dump_root.mkdir(parents=True, exist_ok=True)
    selected_uris = set(task.guide_source_uris)
    written = 0
    for document in generate_seed_guides(task.framework, task.version):
        if selected_uris and document.source_uri not in selected_uris:
            continue
        relative_path = str(document.metadata.get("path") or document.source_uri)
        path = dump_root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(document.raw_text, encoding="utf-8")
        written += 1
    if written:
        subprocess.run(
            ["git", "add", ".k2-demo-confluence-dump"],
            cwd=destination,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            [
                "git",
                "-c",
                "user.name=k2-demo",
                "-c",
                "user.email=k2-demo@example.com",
                "commit",
                "-m",
                "add local confluence dump",
            ],
            cwd=destination,
            check=True,
            capture_output=True,
        )


def _git_diff(worktree: Path) -> str:
    subprocess.run(
        ["git", "add", "-N", "."],
        cwd=worktree,
        text=True,
        capture_output=True,
        check=False,
        timeout=120,
    )
    completed = subprocess.run(
        ["git", "diff", "--binary", "--", *DIFF_PATHSPEC],
        cwd=worktree,
        text=True,
        capture_output=True,
        check=False,
        timeout=120,
    )
    return completed.stdout


def _selected_tasks(args: argparse.Namespace) -> tuple[PatchTask, ...]:
    available = {task.task_id: task for task in patch_tasks(include_kafka=args.include_kafka)}
    if args.task_id:
        missing = [task_id for task_id in args.task_id if task_id not in available]
        if missing:
            raise SystemExit(f"unknown patch task(s): {', '.join(missing)}")
        selected = [available[task_id] for task_id in args.task_id]
    else:
        selected = list(available.values())
    if args.max_tasks:
        selected = selected[: args.max_tasks]
    return tuple(selected)


def _source_root_for_task(task: PatchTask, args: argparse.Namespace) -> Path:
    roots = {
        "flink": args.flink_root or args.source_base / "apache-flink-release-2.2.0",
        "kafka": args.kafka_root or args.source_base / "apache-kafka-4.2",
    }
    return roots[task.source_root_key]


def _is_k2_arm(arm_name: str) -> bool:
    return arm_name.startswith("codex_with_k2_mcp")


def _relative_artifact_path(path: Path, out_dir: Path) -> str:
    try:
        return str(path.relative_to(out_dir))
    except ValueError:
        return str(path)


def _source_roots(args: argparse.Namespace) -> dict[str, str]:
    return {
        "flink": str(args.flink_root or args.source_base / "apache-flink-release-2.2.0"),
        "kafka": str(args.kafka_root or args.source_base / "apache-kafka-4.2"),
    }


def _api_host_override(api_host: str | None) -> tuple[str, ...]:
    return (f'mcp_servers.k2-java-rd.env.K2_API_HOST="{api_host}"',) if api_host else ()


def _validate_live_requirements(args: argparse.Namespace, arms: tuple[str, ...]) -> None:
    if not any(_is_k2_arm(arm_name) for arm_name in arms):
        return
    if args.mcp_backend == "sdk":
        if not os.environ.get("K2_API_KEY"):
            raise SystemExit(
                "K2_API_KEY is required for live K2 SDK arms. "
                "Put it in ignored .env and pass --env-file .env."
            )
        return
    if args.mcp_backend == "kubectl":
        _validate_kubectl_bridge(args)
        return
    if args.mcp_backend == "auto":
        if os.environ.get("K2_API_KEY"):
            return
        _validate_kubectl_bridge(args)


def _validate_kubectl_bridge(args: argparse.Namespace) -> None:
    completed = subprocess.run(
        [
            "kubectl",
            "auth",
            "can-i",
            "get",
            "deployments.apps",
            "-n",
            args.namespace,
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0 or completed.stdout.strip() != "yes":
        reason = (completed.stderr or completed.stdout or "kubectl auth check failed").strip()
        raise SystemExit(
            "kubectl K2 MCP bridge is not usable for live K2 arms: cannot get "
            f"deployments.apps in namespace {args.namespace!r}. {reason}"
        )


def _probe_k2_sdk(args: argparse.Namespace) -> dict[str, Any]:
    if not os.environ.get("K2_API_KEY"):
        raise SystemExit(
            "K2_API_KEY is required for --probe-k2-sdk. "
            "Put it in ignored .env and pass --env-file .env."
        )
    config = K2McpConfig(
        backend="sdk",
        api_key=os.environ.get("K2_API_KEY"),
        api_host=args.api_host or os.environ.get("K2_API_HOST") or os.environ.get("K2_BASE_URL"),
        namespace=args.namespace,
        deployment=args.deployment,
        retrieval_profile=args.retrieval_profile,
        source_base=str(args.source_base),
    )
    server = K2McpServer(config)
    try:
        result = server._search_docs(
            {
                "framework": "flink",
                "api_surface": "rest",
                "query": "Flink REST API JobVertexWatermarksHandler",
                "top_k": 1,
            }
        )
    except Exception as exc:
        raise SystemExit(f"K2 SDK preflight probe failed: {exc}") from exc
    rows = result.get("results") or []
    if not rows:
        raise SystemExit("K2 SDK preflight probe returned no Flink REST results")
    first = rows[0] if isinstance(rows[0], dict) else {}
    return {
        "framework": "flink",
        "result_count": len(rows),
        "first_source_uri": first.get("source_uri"),
        "retrieval_profile": result.get("retrieval_profile"),
    }


def _load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        if not key:
            continue
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--arm", action="append", choices=PATCH_ARM_NAMES)
    parser.add_argument("--task-id", action="append", default=[])
    parser.add_argument("--max-tasks", type=int)
    parser.add_argument("--include-kafka", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--source-base", type=Path, default=DEFAULT_SOURCE_BASE)
    parser.add_argument("--flink-root", type=Path)
    parser.add_argument("--kafka-root", type=Path)
    parser.add_argument("--namespace", default="k2-mvp")
    parser.add_argument("--deployment", default="deploy/k2-mvp-api-internal")
    parser.add_argument("--project-id", default=PROJECT_ID)
    parser.add_argument("--mcp-backend", choices=["sdk", "kubectl", "auto"], default="sdk")
    parser.add_argument("--api-host")
    parser.add_argument("--env-file", type=Path, default=ROOT / ".env")
    parser.add_argument("--retrieval-profile", default="java_exact", choices=sorted(HYBRID_PROFILES))
    parser.add_argument("--model", default="gpt-5.4-mini")
    parser.add_argument("--codex-timeout-s", type=int, default=1800)
    parser.add_argument("--out-dir", type=Path)
    parser.add_argument("--run-tests", action="store_true")
    parser.add_argument("--keep-worktrees", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument(
        "--preflight-only",
        action="store_true",
        help="Validate live K2 requirements and exit before launching Codex.",
    )
    parser.add_argument(
        "--probe-k2-sdk",
        action="store_true",
        help="Run one K2 SDK retrieval probe during preflight or before execution.",
    )
    return parser


if __name__ == "__main__":
    raise SystemExit(main())
