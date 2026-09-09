#!/usr/bin/env python3
"""Validate registry and protocol YAML files against repository schemas."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def validate_file(path: Path, schema: dict) -> list[str]:
    data = load_yaml(path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path))
    rendered = []
    for error in errors:
        location = ".".join(str(p) for p in error.absolute_path) or "<root>"
        rendered.append(f"{path.relative_to(ROOT)}:{location}: {error.message}")
    return rendered


def main() -> int:
    protocol_schema = load_json(ROOT / "schema" / "protocol.schema.json")
    registry_schema = load_json(ROOT / "schema" / "registry.schema.json")

    errors: list[str] = []
    errors.extend(validate_file(ROOT / "registry.yaml", registry_schema))

    registry = load_yaml(ROOT / "registry.yaml")
    seen_ids: set[str] = set()

    for entry in registry.get("protocols", []):
        protocol_id = entry["id"]
        if protocol_id in seen_ids:
            errors.append(f"registry.yaml: duplicate protocol id {protocol_id!r}")
        seen_ids.add(protocol_id)

        protocol_path = ROOT / entry["path"]
        if not protocol_path.is_file():
            errors.append(f"registry.yaml: missing protocol file {entry['path']!r}")
            continue

        errors.extend(validate_file(protocol_path, protocol_schema))
        protocol = load_yaml(protocol_path)

        if protocol.get("protocol_id") != protocol_id:
            errors.append(
                f"{entry['path']}: protocol_id {protocol.get('protocol_id')!r} "
                f"does not match registry id {protocol_id!r}"
            )

        sources = protocol.get("sources", [])
        source_ids = {source["id"] for source in sources}
        if len(source_ids) != len(sources):
            errors.append(f"{entry['path']}: duplicate source id")

        for source_index, source in enumerate(sources):
            source_path = source.get("path")
            if source_path and not (ROOT / source_path).is_file():
                errors.append(
                    f"{entry['path']}:sources[{source_index}]: "
                    f"missing repository source path {source_path!r}"
                )

        transports = protocol.get("transports", [])
        transport_ids = {transport["id"] for transport in transports}
        if len(transport_ids) != len(transports):
            errors.append(f"{entry['path']}: duplicate transport id")

        endpoints_by_transport = {
            transport["id"]: {endpoint["id"] for endpoint in transport.get("endpoints", [])}
            for transport in transports
        }

        message_ids = [message["id"] for message in protocol.get("messages", [])]
        if len(set(message_ids)) != len(message_ids):
            errors.append(f"{entry['path']}: duplicate message id")

        hypothesis_ids = [item["id"] for item in protocol.get("hypotheses", [])]
        if len(set(hypothesis_ids)) != len(hypothesis_ids):
            errors.append(f"{entry['path']}: duplicate hypothesis id")

        def check_evidence(node, location: str):
            if isinstance(node, dict):
                for source_id in node.get("evidence", []) or []:
                    if source_id not in source_ids:
                        errors.append(
                            f"{entry['path']}:{location}: unknown evidence source {source_id!r}"
                        )
                for key, value in node.items():
                    check_evidence(value, f"{location}.{key}")
            elif isinstance(node, list):
                for index, value in enumerate(node):
                    check_evidence(value, f"{location}[{index}]")

        check_evidence(protocol, "<root>")

        if protocol.get("contract_revision") != entry.get("contract_revision"):
            errors.append(
                f"{entry['path']}: contract_revision {protocol.get('contract_revision')!r} "
                f"does not match registry revision {entry.get('contract_revision')!r}"
            )

        protocol_transport_kinds = {transport["kind"] for transport in transports}
        if set(entry.get("transports", [])) != protocol_transport_kinds:
            errors.append(
                f"{entry['path']}: registry transports do not match protocol transport kinds"
            )

        for index, message in enumerate(protocol.get("messages", [])):
            transport_id = message["transport"]
            if transport_id not in transport_ids:
                errors.append(
                    f"{entry['path']}:messages[{index}]: unknown transport {transport_id!r}"
                )
                continue
            if message["endpoint"] not in endpoints_by_transport.get(transport_id, set()):
                errors.append(
                    f"{entry['path']}:messages[{index}]: endpoint {message['endpoint']!r} "
                    f"does not exist on transport {transport_id!r}"
                )

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validated {len(seen_ids)} protocol(s) successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
