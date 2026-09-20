# Cobra RAD 700i protocol

**Protocol ID:** `cobra.rad-700i`  
**Coverage:** Partial  
**Known transport:** Bluetooth Low Energy

This directory documents the public state of RAD 700i protocol research. The canonical machine-readable contract is [`protocol.yaml`](protocol.yaml).

## Currently documented

- Cobra primary BLE service and protocol/GPS characteristic UUIDs.
- Observed GATT/ATT handles from physical-device implementations/captures, treated as non-stable observations.
- F5 companion-protocol framing on a physical RAD 700i.
- Bidirectional Drive Smarter authentication/session traffic (`A3/A2/A5` and detector-originated `A1/A4/A3`).
- Observed Status, model, version, GPS-equipped, display-capabilities, and display-length exchanges.
- Recurring Drive Smarter speed-limit/current-speed updates (`A9`/`AA`) with compatible-family payload interpretation.
- Candidate X/K/Ka/Laser/POP alert byte values and signal-strength byte.
- Candidate GPS payload layout.

The 2026-09-11 capture identifies the tested detector as `RAD 700i` and includes a version response containing `M1.2.3.6`.

## Still incomplete

Among other things:

- Exact radar-frequency representation and richer alert metadata.
- Controlled validation of `DISPLAY_MESSAGE (0x9A)` and client `PLAY_TONE (0x9B)` on this model.
- One-setting-at-a-time mapping of detector settings and sensitivity/mode synchronization.
- Mute/lockout/mark synchronization.
- Defender/community alert exchange.
- Firmware-update transport and firmware-specific differences.
- Controlled GPS payload validation.

## Status discipline

Direct RAD 700i observations and compatible-family semantic corroboration are kept separate. The Drive Smarter HCI capture promotes F5 framing and several command exchanges to observed status, but it does not justify promoting commands that were not exercised.

See [`packets.md`](packets.md), [`characteristics.md`](characteristics.md), and [`captures/2026-09-11-drive-smarter-session.md`](captures/2026-09-11-drive-smarter-session.md).

## Acknowledgement

Initial BLE observations were seeded from [`grabercn/Car-HUD`](https://github.com/grabercn/Car-HUD). Command naming and challenge/response behavior are additionally cross-checked against [`qoq/esclib.github.io`](https://github.com/qoq/esclib.github.io). The new F5/session evidence comes from a sanitized physical RAD 700i Drive Smarter capture. See [`sources.md`](sources.md) for provenance.
