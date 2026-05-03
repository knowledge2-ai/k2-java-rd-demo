"""Duck-typed K2 Agent and Knowledge Feed runtime helpers."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from copy import deepcopy
from typing import Any, Literal

from .agent_specs import build_agent_specs, default_corpus_placeholders


def validate_corpus_ids(specs: Mapping[str, Any]) -> None:
    """Ensure every corpus used by agents and feeds has a concrete ID."""
    missing: set[str] = set()
    corpora = specs.get("corpora", {})
    if not isinstance(corpora, Mapping):
        raise ValueError("corpora must be a mapping")
    corpus_name_by_id = {
        str(corpus_id): str(corpus_name)
        for corpus_name, corpus_id in corpora.items()
    }

    agents = specs.get("agents", {})
    if not isinstance(agents, Mapping):
        raise ValueError("agent specs must be a mapping")
    for agent_key, agent_spec in agents.items():
        if not isinstance(agent_spec, Mapping):
            raise ValueError(f"agent {agent_key!r} must be a mapping")
        corpus_id = agent_spec.get("corpus_id")
        if _is_missing_corpus_id(corpus_id):
            missing.add(_corpus_label(corpus_id, corpus_name_by_id, f"{agent_key}.corpus_id"))

    feeds = specs.get("feeds", {})
    if not isinstance(feeds, Mapping):
        raise ValueError("feed specs must be a mapping")
    for feed_key, feed_spec in feeds.items():
        if not isinstance(feed_spec, Mapping):
            raise ValueError(f"feed {feed_key!r} must be a mapping")
        target_corpus = feed_spec.get("target_corpus")
        if not isinstance(target_corpus, Mapping) or "existing" not in target_corpus:
            raise ValueError(f"feed {feed_key!r} must target an existing corpus")
        corpus_id = target_corpus.get("existing")
        if _is_missing_corpus_id(corpus_id):
            missing.add(_corpus_label(corpus_id, corpus_name_by_id, f"{feed_key}.target_corpus"))

    if missing:
        names = ", ".join(sorted(missing))
        raise ValueError(f"missing concrete corpus IDs for: {names}")


def resolve_source_agent_keys(
    agent_spec: Mapping[str, Any],
    agent_ids: Mapping[str, str],
) -> dict[str, Any]:
    """Replace logical source_agent_keys entries with concrete agent IDs."""
    payload = deepcopy(dict(agent_spec))
    references = payload.pop("source_agent_keys", [])
    if references:
        payload["source_agents"] = [
            _resolve_source_reference(reference, agent_ids) for reference in references
        ]
    return payload


def create_agents(
    client: Any,
    agent_specs: Mapping[str, Mapping[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Create agents in dependency order and return created IDs by logical key."""
    created: dict[str, dict[str, Any]] = {}
    for agent_key in _agent_creation_order(agent_specs):
        agent_ids = {key: value["id"] for key, value in created.items()}
        payload = resolve_source_agent_keys(agent_specs[agent_key], agent_ids)
        response = _call_resource_method(
            client,
            direct_name="create_agent",
            namespace_name="agents",
            namespace_method_name="create",
            payload=payload,
        )
        created[agent_key] = {
            "id": _extract_resource_id(response, resource_name="agent"),
            "name": str(payload.get("name", agent_key)),
            "activated": False,
            "source_agent_ids": [
                source["agent_id"] for source in payload.get("source_agents", [])
            ],
        }
    return created


def activate_agents(client: Any, created_agents: dict[str, dict[str, Any]]) -> None:
    """Activate every created agent in creation order."""
    for agent in created_agents.values():
        _call_resource_method(
            client,
            direct_name="activate_agent",
            namespace_name="agents",
            namespace_method_name="activate",
            payload={"agent_id": agent["id"]},
        )
        agent["activated"] = True


def create_feeds(
    client: Any,
    feed_specs: Mapping[str, Mapping[str, Any]],
    agent_ids: Mapping[str, str],
) -> dict[str, dict[str, Any]]:
    """Create Knowledge Feeds after their source agents have concrete IDs."""
    created: dict[str, dict[str, Any]] = {}
    for feed_key, feed_spec in feed_specs.items():
        payload = _resolve_feed_spec(feed_key, feed_spec, agent_ids)
        response = _call_resource_method(
            client,
            direct_name="create_feed",
            namespace_name="feeds",
            namespace_method_name="create",
            payload=payload,
        )
        created[feed_key] = {
            "id": _extract_resource_id(response, resource_name="feed"),
            "name": str(payload.get("name", feed_key)),
            "source_agent_id": payload["source_agent_id"],
            "target_corpus_id": payload["target_corpus_id"],
            "dry_run": None,
        }
    return created


def _unwrap_list_result(result: Any) -> list[Any]:
    """Normalise a list-method return value to a plain list."""
    if isinstance(result, list):
        return result
    return list(getattr(result, "items", None) or getattr(result, "data", None) or [])


def _list_resources(
    client: Any,
    *,
    direct_name: str,
    namespace_name: str,
    namespace_method_name: str,
) -> list[Any]:
    """List existing resources via the duck-typed client.

    Raises ``RuntimeError`` when no list method is available — callers
    in ensure mode must not silently fall through to create-all.
    """
    direct_method = getattr(client, direct_name, None)
    if callable(direct_method):
        return _unwrap_list_result(direct_method())

    namespace = getattr(client, namespace_name, None)
    namespace_method = getattr(namespace, namespace_method_name, None)
    if callable(namespace_method):
        return _unwrap_list_result(namespace_method())

    raise RuntimeError(
        f"client has no {direct_name}() or {namespace_name}.{namespace_method_name}() method; "
        f"ensure mode requires list support to prevent duplicate creation"
    )


def _find_existing_by_name(
    resources: list[Any], name: str,
) -> dict[str, Any] | None:
    """Find an existing resource by name in a list of resources."""
    for resource in resources:
        resource_name = (
            resource.get("name") if isinstance(resource, Mapping)
            else getattr(resource, "name", None)
        )
        if resource_name == name:
            if isinstance(resource, Mapping):
                return dict(resource)
            return {"id": getattr(resource, "id", None), "name": resource_name}
    return None


def ensure_agents(
    client: Any,
    agent_specs: Mapping[str, Mapping[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Create agents, reusing existing ones that match by name.

    If listing fails, the exception propagates rather than falling back to
    create-all, which would risk duplicating existing resources.
    """
    existing = _list_resources(
        client,
        direct_name="list_agents",
        namespace_name="agents",
        namespace_method_name="list",
    )

    created: dict[str, dict[str, Any]] = {}
    for agent_key in _agent_creation_order(agent_specs):
        agent_name = str(agent_specs[agent_key].get("name", agent_key))
        found = _find_existing_by_name(existing, agent_name)
        if found and found.get("id"):
            created[agent_key] = {
                "id": str(found["id"]),
                "name": agent_name,
                "activated": True,
                "source_agent_ids": [],
                "reused": True,
            }
            continue

        agent_ids = {key: value["id"] for key, value in created.items()}
        payload = resolve_source_agent_keys(agent_specs[agent_key], agent_ids)
        response = _call_resource_method(
            client,
            direct_name="create_agent",
            namespace_name="agents",
            namespace_method_name="create",
            payload=payload,
        )
        created[agent_key] = {
            "id": _extract_resource_id(response, resource_name="agent"),
            "name": agent_name,
            "activated": False,
            "source_agent_ids": [
                source["agent_id"] for source in payload.get("source_agents", [])
            ],
            "reused": False,
        }
    return created


def ensure_feeds(
    client: Any,
    feed_specs: Mapping[str, Mapping[str, Any]],
    agent_ids: Mapping[str, str],
) -> dict[str, dict[str, Any]]:
    """Create feeds, reusing existing ones that match by name.

    If listing fails, the exception propagates rather than falling back to
    create-all, which would risk duplicating existing resources.

    Reused feeds report ``source_agent_id`` and ``target_corpus_id`` as
    ``None`` because the list endpoint may not include these fields.
    """
    existing = _list_resources(
        client,
        direct_name="list_feeds",
        namespace_name="feeds",
        namespace_method_name="list",
    )

    created: dict[str, dict[str, Any]] = {}
    for feed_key, feed_spec in feed_specs.items():
        feed_name = str(feed_spec.get("name", feed_key))
        found = _find_existing_by_name(existing, feed_name)
        if found and found.get("id"):
            created[feed_key] = {
                "id": str(found["id"]),
                "name": feed_name,
                "source_agent_id": None,
                "target_corpus_id": None,
                "dry_run": None,
                "reused": True,
            }
            continue

        payload = _resolve_feed_spec(feed_key, feed_spec, agent_ids)
        response = _call_resource_method(
            client,
            direct_name="create_feed",
            namespace_name="feeds",
            namespace_method_name="create",
            payload=payload,
        )
        created[feed_key] = {
            "id": _extract_resource_id(response, resource_name="feed"),
            "name": feed_name,
            "source_agent_id": payload["source_agent_id"],
            "target_corpus_id": payload["target_corpus_id"],
            "dry_run": None,
            "reused": False,
        }
    return created


def run_feeds_dry_run(client: Any, created_feeds: dict[str, dict[str, Any]]) -> None:
    """Run created feeds in dry-run mode and attach the responses to the summary."""
    for feed in created_feeds.values():
        feed["dry_run"] = _call_resource_method(
            client,
            direct_name="run_feed",
            namespace_name="feeds",
            namespace_method_name="run",
            payload={"feed_id": feed["id"], "dry_run": True},
        )


def deploy_agents_and_feeds(
    client: Any,
    *,
    project_id: str = "<java-rd-demo-project-id>",
    corpus_ids: Mapping[str, str] | None = None,
    specs: Mapping[str, Any] | None = None,
    activate: bool = True,
    run_feed_dry_run: bool = False,
    create_mode: Literal["create", "ensure"] = "ensure",
) -> dict[str, Any]:
    """Deploy the demo Agents and Knowledge Feeds using a duck-typed client.

    When *create_mode* is ``"ensure"`` (the default), existing agents and feeds
    with matching names are reused instead of creating duplicates.
    """
    if specs is None:
        selected_specs = build_agent_specs(
            project_id=project_id,
            corpus_ids=dict(corpus_ids or {}),
        )
    else:
        selected_specs = deepcopy(specs)
    validate_corpus_ids(selected_specs)

    if create_mode == "ensure":
        agents = ensure_agents(client, selected_specs["agents"])
    else:
        agents = create_agents(client, selected_specs["agents"])
    if activate:
        agents_to_activate = {
            key: agent for key, agent in agents.items()
            if not agent.get("reused", False) and not agent.get("activated", False)
        }
        if agents_to_activate:
            activate_agents(client, agents_to_activate)

    agent_ids = {agent_key: agent["id"] for agent_key, agent in agents.items()}
    if create_mode == "ensure":
        feeds = ensure_feeds(client, selected_specs["feeds"], agent_ids)
    else:
        feeds = create_feeds(client, selected_specs["feeds"], agent_ids)
    if run_feed_dry_run:
        run_feeds_dry_run(client, feeds)

    return {
        "project_id": selected_specs["project_id"],
        "corpora": deepcopy(selected_specs["corpora"]),
        "agents": deepcopy(agents),
        "feeds": deepcopy(feeds),
    }


def _is_missing_corpus_id(value: Any) -> bool:
    if not isinstance(value, str):
        return True
    stripped = value.strip()
    return not stripped or (stripped.startswith("<") and stripped.endswith(">"))


def _corpus_label(value: Any, corpus_name_by_id: Mapping[str, str], fallback: str) -> str:
    if isinstance(value, str):
        if value in corpus_name_by_id:
            return corpus_name_by_id[value]
        for corpus_name, placeholder in default_corpus_placeholders().items():
            if value == placeholder:
                return corpus_name
    return fallback


def _source_agent_keys(agent_spec: Mapping[str, Any]) -> list[str]:
    references = agent_spec.get("source_agent_keys", [])
    if not references:
        return []
    if isinstance(references, (str, bytes)) or not isinstance(references, Iterable):
        raise ValueError("source_agent_keys must be an iterable")

    keys: list[str] = []
    for reference in references:
        if isinstance(reference, str):
            keys.append(reference)
            continue
        if isinstance(reference, Mapping):
            agent_key = reference.get("agent_key")
            if isinstance(agent_key, str) and agent_key:
                keys.append(agent_key)
                continue
        raise ValueError(f"invalid source agent reference: {reference!r}")
    return keys


def _agent_creation_order(agent_specs: Mapping[str, Mapping[str, Any]]) -> list[str]:
    order: list[str] = []
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(agent_key: str) -> None:
        if agent_key in visited:
            return
        if agent_key in visiting:
            raise ValueError(f"source agent cycle includes {agent_key!r}")
        if agent_key not in agent_specs:
            raise ValueError(f"unknown source agent key: {agent_key}")

        visiting.add(agent_key)
        for source_agent_key in _source_agent_keys(agent_specs[agent_key]):
            visit(source_agent_key)
        visiting.remove(agent_key)
        visited.add(agent_key)
        order.append(agent_key)

    for agent_key in agent_specs:
        visit(agent_key)
    return order


def _resolve_source_reference(reference: Any, agent_ids: Mapping[str, str]) -> dict[str, Any]:
    if isinstance(reference, str):
        agent_key = reference
        resolved: dict[str, Any] = {}
    elif isinstance(reference, Mapping):
        agent_key = reference.get("agent_key")
        resolved = {
            str(key): deepcopy(value)
            for key, value in reference.items()
            if key != "agent_key"
        }
    else:
        raise ValueError(f"invalid source agent reference: {reference!r}")

    if not isinstance(agent_key, str) or not agent_key:
        raise ValueError(f"invalid source agent reference: {reference!r}")
    if agent_key not in agent_ids:
        raise ValueError(f"source agent {agent_key!r} has not been created")

    resolved["agent_id"] = agent_ids[agent_key]
    return resolved


def _resolve_feed_spec(
    feed_key: str,
    feed_spec: Mapping[str, Any],
    agent_ids: Mapping[str, str],
) -> dict[str, Any]:
    payload = deepcopy(dict(feed_spec))
    source_agent_key = payload.pop("source_agent_key", None)
    if not isinstance(source_agent_key, str) or source_agent_key not in agent_ids:
        raise ValueError(f"feed {feed_key!r} references unknown source agent {source_agent_key!r}")

    target_corpus = payload.get("target_corpus")
    if not isinstance(target_corpus, Mapping) or _is_missing_corpus_id(
        target_corpus.get("existing")
    ):
        raise ValueError(f"feed {feed_key!r} must target an existing corpus")

    payload["source_agent_id"] = agent_ids[source_agent_key]
    payload["target_corpus_id"] = str(target_corpus["existing"])
    return payload


def _call_resource_method(
    client: Any,
    *,
    direct_name: str,
    namespace_name: str,
    namespace_method_name: str,
    payload: Mapping[str, Any],
) -> Any:
    direct_method = getattr(client, direct_name, None)
    if callable(direct_method):
        return direct_method(**dict(payload))

    namespace = getattr(client, namespace_name, None)
    namespace_method = getattr(namespace, namespace_method_name, None)
    if callable(namespace_method):
        return namespace_method(**dict(payload))

    raise AttributeError(
        f"client must provide {direct_name}() or {namespace_name}.{namespace_method_name}()"
    )


def _extract_resource_id(response: Any, *, resource_name: str) -> str:
    id_fields = (f"{resource_name}_id", "id")
    if isinstance(response, str) and response:
        return response

    if isinstance(response, Mapping):
        for field in id_fields:
            value = response.get(field)
            if value:
                return str(value)
        nested = response.get(resource_name)
        if isinstance(nested, Mapping):
            for field in id_fields:
                value = nested.get(field)
                if value:
                    return str(value)

    for field in id_fields:
        value = getattr(response, field, None)
        if value:
            return str(value)

    nested = getattr(response, resource_name, None)
    if nested is not None:
        for field in id_fields:
            value = getattr(nested, field, None)
            if value:
                return str(value)

    raise ValueError(f"{resource_name} create response did not include an ID")
