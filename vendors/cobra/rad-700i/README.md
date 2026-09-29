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
- Physical toolbox validation that `PLAY_TONE (0x9B)` values `1` and `2` produce audible tones while value `0` produced no audible output on the tested unit.
- Physical toolbox validation that `A9` can update the posted speed-limit display; `AA` produced no visible current-speed override in the stationary test.
- Periodic detector protocol traffic including no-alert `F5 01 82`, `F5 01 A7`, and variable Status values including `0x0B`.
- Candidate X/K/Ka/Laser/POP alert byte values and signal-strength byte.
- Candidate GPS payload layout.

The 2026-09-11 capture identifies the tested detector as `RAD 700i` and includes a version response containing `M1.2.3.6`.

## Still incomplete

Among other things:

- Exact radar-frequency representation and richer alert metadata.
- Determine why the compatible-family `DISPLAY_MESSAGE (0x9A)` format produced no visible display change on the tested RAD 700i.
- Characterize the exact meanings of `PLAY_TONE (0x9B)` payload values `0`, `1`, and `2`; values `1` and `2` are now audibly confirmed.
- One-setting-at-a-time mapping of detector settings and sensitivity/mode synchronization.
- Mute/lockout/mark synchronization.
- Defender/community alert exchange.
- Firmware-update transport and firmware-specific differences.
- Controlled GPS payload validation.

## Status discipline

Direct RAD 700i observations and compatible-family semantic corroboration are kept separate. The Drive Smarter HCI capture promotes F5 framing and several command exchanges to observed status, but it does not justify promoting commands that were not exercised.

See [`packets.md`](packets.md), [`characteristics.md`](characteristics.md), [`captures/2026-09-11-drive-smarter-session.md`](captures/2026-09-11-drive-smarter-session.md), and [`captures/2026-09-29-toolbox-observations.md`](captures/2026-09-29-toolbox-observations.md).

## Acknowledgement

Initial BLE observations were seeded from [`grabercn/Car-HUD`](https://github.com/grabercn/Car-HUD). Command naming and challenge/response behavior are additionally cross-checked against [`qoq/esclib.github.io`](https://github.com/qoq/esclib.github.io). The new F5/session evidence comes from a sanitized physical RAD 700i Drive Smarter capture. See [`sources.md`](sources.md) for provenance.
