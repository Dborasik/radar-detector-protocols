# Contributing

Contributions are accepted for new detectors, corrections, additional packet decoding, firmware-specific behavior, sanitized captures, and better evidence for existing claims.

## Ground rules

1. **Do not present guesses as facts.** Use the confidence vocabulary in `docs/CONFIDENCE.md`.
2. **Provide provenance.** Link public sources or describe the test/capture that produced the observation.
3. **State hardware and firmware scope.** A protocol may change between revisions.
4. **Do not submit confidential or improperly obtained vendor material.** Public documentation, your own observations, and material you are authorized to share are acceptable.
5. **Do not copy third-party source code unless its license allows it.** Prefer documenting the protocol fact and citing the implementation that demonstrated it.
6. **Sanitize captures.** Remove or redact persistent device addresses, serial numbers, account identifiers, GPS positions, tokens, and other personal or secret data unless they are essential and safe to publish.
7. **Keep captures raw.** Do not modify payload bytes merely to make them fit a theory; store redaction metadata separately.

## New detector checklist

Create:

```text
vendors/<vendor>/<model>/
├── README.md
├── protocol.yaml
├── characteristics.md
├── packets.md
├── sources.md
├── captures/README.md
└── examples/README.md
```

Then add it to `registry.yaml`.

## Stable identifiers

- Vendor/model directory names: lowercase kebab-case.
- Protocol ID: `<vendor-slug>.<model-slug>`.
- Transport IDs inside a protocol: short stable IDs such as `ble-main`, `usb-service`, or `wifi-api`.
- Message IDs: descriptive kebab-case such as `radar-alert` or `settings-write`.

Do not rename an established protocol ID simply for aesthetics. If hardware is protocol-incompatible, create a new entry or variant.

## Evidence

Every meaningful field may contain an `evidence` array referring to IDs in `protocol.yaml -> sources`.

Preferred evidence, roughly strongest first:

1. Published manufacturer/developer documentation.
2. Multiple independent physical-device reproductions.
3. A physical-device capture with documented test conditions.
4. A working public implementation tested against real hardware.
5. Static analysis/decompilation or client behavior without physical-device validation.
6. Reasoned hypothesis.

Evidence strength and confidence are related but not identical. Maintainers may lower a confidence level when provenance does not justify it.

## Captures

Place sanitized raw captures under `captures/` and include adjacent metadata, for example:

```text
captures/
├── 2026-09-07-ka-alert.pcapng
└── 2026-09-07-ka-alert.yaml
```

Metadata should record detector model, hardware revision if known, firmware version if known, host/phone platform, capture tool, test action, transport, redactions, and SHA-256 of the original capture if the published copy was sanitized.

## Validation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
python scripts/validate.py
```

CI performs the same structural checks on pull requests.

## Contribution license

By submitting a contribution, you agree that your contribution may be distributed under the repository's MIT License and that you have the right to submit it.
