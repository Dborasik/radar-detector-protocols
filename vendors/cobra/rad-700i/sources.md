# Sources and provenance

## `car-hud-implementation`

**Car-HUD**, by GitHub user [`grabercn`](https://github.com/grabercn)  
Repository: https://github.com/grabercn/Car-HUD  
Seed implementation inspected: https://github.com/grabercn/Car-HUD/blob/a5692f7a0260cc787a0b6cee7db1a908c3255520/src/cobra_service.py

The project reports successfully connecting to a physical Cobra RAD 700i over BLE and subscribing to radar-alert and GPS characteristics. This repository uses that work as **provenance for initial protocol observations** rather than copying its implementation.

Credited observations seeded from it include:

- alert characteristic UUID
- GPS characteristic UUID
- reported read/notify behavior
- observed GATT handles
- alert band-code mapping used by the implementation
- candidate signal-strength interpretation
- candidate GPS parsing logic

Because the source repository does not itself constitute independent reproduction by this project, interpretations are assigned conservative confidence levels.

## `cobra-product-page`

Cobra RAD 700i official product page: https://www.cobra.com/products/rad700i

Used only for vendor-confirmed product context such as RAD 700i Bluetooth and Drive Smarter support.

## Adding sources

Prefer stable permalinks/commit hashes for code. For experiments or captures, add a source entry to `protocol.yaml` and link the corresponding file under `captures/`.
