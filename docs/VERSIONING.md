# Versioning

Two different versions are tracked.

## `schema_version`

Describes the repository contract format itself. It changes only when the YAML schema changes in a way consumers need to understand.

- Backward-compatible schema additions may retain the same major schema version.
- Breaking structural changes require a new major schema version and migration guidance.

## `contract_revision`

Each detector protocol has an integer `contract_revision` beginning at `1`.

Increment it whenever the machine-readable meaning of that detector's `protocol.yaml` changes, including:

- new endpoints/messages/fields
- corrected values or field semantics
- confidence promotion/demotion
- changed firmware scope
- removed or superseded claims

Pure Markdown wording/formatting changes do not require a revision bump when `protocol.yaml` is unchanged.

The same revision is mirrored in `registry.yaml` and checked by validation.

## Protocol IDs

A protocol ID is stable. Do not rename it for cosmetic reasons.

If a hardware or firmware generation is materially incompatible, model it explicitly as a new protocol entry or documented variant instead of rewriting history under the old ID.

For reproducible software builds, consumers should pin a Git commit/tag in addition to checking `contract_revision`.
