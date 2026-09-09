# Cobra RAD 700i protocol

**Protocol ID:** `cobra.rad-700i`  
**Coverage:** Partial  
**Known transport:** Bluetooth Low Energy

This directory documents the public state of RAD 700i protocol research. The canonical machine-readable contract is [`protocol.yaml`](protocol.yaml).

## Currently documented

- BLE alert characteristic UUID.
- BLE GPS characteristic UUID.
- Observed GATT handles from one public implementation, treated as non-stable observations.
- Candidate X/K/Ka/Laser/POP alert byte values.
- Candidate signal-strength byte.
- Candidate GPS payload layout.

## Not yet documented

Among other things:

- Complete GATT service/descriptor map.
- Pairing/authentication/session setup behavior.
- Exact radar frequency representation.
- Alert metadata beyond the currently observed bytes.
- Reads/writes for detector configuration.
- Sensitivity/mode synchronization.
- Mute/lockout/mark synchronization.
- Defender/community alert exchange.
- Firmware update transport.
- Firmware-specific protocol differences.

## Status discipline

The existing public implementation is enough to seed the registry, but not enough to call the protocol complete. In particular, the signal-strength interpretation and GPS field layout need controlled captures before promotion to stronger confidence levels.

See [`packets.md`](packets.md) and [`characteristics.md`](characteristics.md).

## Acknowledgement

Initial BLE observations were seeded from [`grabercn/Car-HUD`](https://github.com/grabercn/Car-HUD), whose public RAD 700i service reports a successful physical-device connection and alert/GPS subscriptions. See [`sources.md`](sources.md) for exact provenance. No Car-HUD source code is included here.
