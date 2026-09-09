# Radar Detector Protocols

A public, vendor-neutral registry of documented and reverse-engineered radar detector communication protocols.

The repository stores **protocol contracts and evidence**, not application code. Its purpose is to make interoperable implementations possible without forcing every project to rediscover the same wire formats.

## Principles

- Facts and hypotheses are kept separate.
- Every non-trivial claim should have provenance.
- Firmware/model scope must be explicit.
- Raw captures are welcome when they can be shared safely and legally.
- Contributions should improve interoperability, documentation, or reproducibility.
- Vendor trademarks belong to their respective owners; this project is not affiliated with or endorsed by any detector manufacturer.

## Registry

| Vendor | Model | Protocol ID | Transport | Coverage | Spec |
|---|---|---|---|---|---|
| Cobra | RAD 700i | `cobra.rad-700i` | Bluetooth Low Energy | Partial | [`vendors/cobra/rad-700i/`](vendors/cobra/rad-700i/) |

Machine-readable index: [`registry.yaml`](registry.yaml)

## Repository layout

```text
.
├── registry.yaml                 # Machine-readable device/protocol index
├── schema/                       # Schemas that every protocol entry must follow
├── docs/                         # Repository-wide documentation conventions
├── vendors/
│   └── <vendor>/
│       └── <model>/
│           ├── README.md         # Human-readable protocol overview
│           ├── protocol.yaml     # Canonical machine-readable contract
│           ├── packets.md        # Detailed packet/message notes
│           ├── characteristics.md# Transport-specific endpoint notes
│           ├── sources.md        # Provenance and acknowledgements
│           ├── captures/         # Sanitized raw captures + metadata
│           └── examples/         # Annotated examples, never fabricated captures
├── scripts/validate.py           # Contract validation
└── .github/                      # PR/issue templates, ownership, and CI
```

## Confidence levels

Protocol fields use one of these confidence levels:

- `confirmed` — independently reproduced or supported by authoritative documentation.
- `observed` — directly observed on a real device or in a working implementation, but not yet independently reproduced here.
- `inferred` — interpretation strongly suggested by observations but not fully isolated/verified.
- `hypothesis` — plausible working theory requiring testing.
- `disputed` — conflicting evidence exists.
- `unknown` — intentionally undocumented/undetermined.

See [`docs/CONFIDENCE.md`](docs/CONFIDENCE.md). Contract/schema versioning is defined in [`docs/VERSIONING.md`](docs/VERSIONING.md).

## Contributing

Contributions are expected to come through pull requests, including contributions from forks. Every contribution must include enough evidence to justify the documented confidence level and must pass repository validation.

`@Dborasik` is the repository code owner. Contributor pull requests require a current-head approval from the repository owner before they are considered merge-ready. See [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`.github/REPOSITORY_SETTINGS.md`](.github/REPOSITORY_SETTINGS.md).

To add a detector:

1. Copy the closest existing vendor/model directory.
2. Choose a stable protocol ID: `<vendor-slug>.<model-slug>`.
3. Fill in `protocol.yaml`.
4. Add human-readable notes and sources.
5. Add the device to `registry.yaml`.
6. Run `python scripts/validate.py`.
7. Open a PR with evidence and firmware/hardware scope.

## License

Licensed under the **Apache License 2.0**. See [`LICENSE`](LICENSE) and [`NOTICE.md`](NOTICE.md).
