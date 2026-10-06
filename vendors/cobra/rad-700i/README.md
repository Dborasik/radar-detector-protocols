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
- Exact read-only Drive Smarter inventory exchanges for current/supported band masks (`86/8C`, `8C/8F`) and marker masks (`92/97`, `95/9B`).
- Exact setting IDs queried by Drive Smarter on the tested RAD 700i, including model-specific IDs above the older compatible-family `0x1B` range.
- Drive Smarter 4.12 resolution of observed zero-payload `AF` as the radar enable/disable support query and exact `D1 00` as `getRadarOptions(ALL)`; state-changing `D0` remains blocked.
- Current Drive Smarter 4.12 alert record decoder: 4-byte `0x82` and 5-byte `0xA9` records, exact band extraction, frequency assembly, front/rear signal-strength masks, numeric direction extraction, Laser subtype, lockout behavior, and first-qualifying-record app selection.
- Current Drive Smarter band-enable byte/mask map, applied to the physically observed RAD 700i current/supported mask.
- Current Drive Smarter marker-enable byte/mask map, applied to the physically observed RAD 700i marker masks.
- Exact current-app radar-option IDs, filter values, and passive `AC/AE` response layouts.
- Exact current-app `DISPLAY_LOCATION (0xAD)` five-byte packer and `DISPLAY_CLEAR_LOCATION (0xAE)` construction, with physical RAD 700i capability bit `0x04` present but no live location-display validation yet.
- Current Drive Smarter turn-by-turn UUID family, framing, capability negotiation, maneuver payload structure, maneuver types/modifiers, ETA/lane fields, and checksum construction; physical RAD 700i support remains unverified.
- Additional setting-value labels derived from the current app and applied conservatively to physically observed values, including the unresolved Sensitivity `0x10` mismatch.
- Candidate GPS payload layout.

The 2026-09-11 capture identifies the tested detector as `RAD 700i` and includes a version response containing `M1.2.3.6`.

## Still incomplete

Among other things:

- Physical RAD 700i validation of at least one non-empty active-alert record; the current Drive Smarter application decoder itself is now documented.
- Determine why the compatible-family `DISPLAY_MESSAGE (0x9A)` format produced no visible display change on the tested RAD 700i.
- Characterize the exact meanings of `PLAY_TONE (0x9B)` payload values `0`, `1`, and `2`; values `1` and `2` are now audibly confirmed.
- Physical correlation of the remaining ambiguous setting values, especially Sensitivity `0x10` and AutoLearn; many other physically observed values now have exact current-app labels.
- Physical RAD 700i radar-option response capture and model validation of per-option `D3` information requests; exact current-app option IDs/parsers are now known.
- Physical validation of `DISPLAY_LOCATION (0xAD)` / clear-location behavior. The current app packer is now exact and the detector advertises the display-location capability bit.
- Determine whether the physical RAD 700i exposes the current app's separate turn-by-turn BLE service and, if so, validate capability/maneuver packets before enabling live navigation writes.
- Mute/lockout/mark synchronization.
- Defender/community alert exchange beyond the now-reduced detector display-location packer.
- Firmware-update transport and firmware-specific differences.
- Controlled GPS payload validation.

## Status discipline

Direct RAD 700i observations and compatible-family semantic corroboration are kept separate. The Drive Smarter HCI capture promotes F5 framing and several command exchanges to observed status, but it does not justify promoting commands that were not exercised.

See [`packets.md`](packets.md), [`characteristics.md`](characteristics.md), [`captures/2026-09-11-drive-smarter-session.md`](captures/2026-09-11-drive-smarter-session.md), and [`captures/2026-09-29-toolbox-observations.md`](captures/2026-09-29-toolbox-observations.md).

## Acknowledgement

Initial BLE observations were seeded from [`grabercn/Car-HUD`](https://github.com/grabercn/Car-HUD). Command naming and challenge/response behavior are additionally cross-checked against [`qoq/esclib.github.io`](https://github.com/qoq/esclib.github.io). The new F5/session evidence comes from a sanitized physical RAD 700i Drive Smarter capture. See [`sources.md`](sources.md) for provenance.
