# Protocol format

`protocol.yaml` is the canonical machine-readable contract. Markdown files explain context, experiments, ambiguities, and history.

## Required top-level fields

- `schema_version`
- `protocol_id`
- `vendor`
- `device`
- `coverage`
- `transports`
- `messages`
- `sources`
- `last_updated`

## Transport-neutral design

The registry must support more than BLE. A detector may expose one or more transports such as:

- Bluetooth Low Energy
- Bluetooth Classic / RFCOMM
- USB
- serial/UART
- Wi-Fi/TCP
- Wi-Fi/UDP
- HTTP/WebSocket
- proprietary accessory buses

Transport-specific details belong under each transport entry. Message semantics belong under `messages` and reference a transport/end-point.

## GATT handles

BLE attribute handles are observations, not stable protocol identifiers. Firmware can reorder the GATT table. UUIDs should be treated as canonical when available; observed handles belong in `observed_handles` with firmware scope.

## Reserved and unknown data

Unknown bytes should remain explicit. Do not silently discard them from packet diagrams. Use `unknown` or `reserved` names and a low confidence level until their behavior is understood.

## Evidence sources

A source may point to either a public `url` or a repository-relative `path`. Use `path` for committed captures, experiment notes, or other in-repository evidence so contributors do not need to fabricate a GitHub URL before a PR exists. Repository-relative paths are validated for existence.
