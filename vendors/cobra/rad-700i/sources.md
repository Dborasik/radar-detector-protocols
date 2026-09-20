# Sources and provenance

## `drive-smarter-capture-2026-09-11`

Sanitized evidence summary: [`captures/2026-09-11-drive-smarter-session.md`](captures/2026-09-11-drive-smarter-session.md)

The source was an Android Bluetooth HCI snoop capture made while Drive Smarter connected normally to a physical Cobra RAD 700i. The raw system-wide HCI log is not committed because it can contain unrelated Bluetooth-device traffic. The protocol repository records only the filtered/sanitized RAD 700i evidence and the SHA-256 of the filtered CSV used for analysis.

Direct observations include:

- client TX characteristic UUID/handle association
- detector RX characteristic traffic
- F5 framing
- client-originated and detector-originated authentication exchanges
- status/model/version/GPS/display query responses
- recurring `A9` and `AA` writes during normal Drive Smarter operation
- settings-query synchronization traffic

## `esclib-compatible-protocol`

Repository: https://github.com/qoq/esclib.github.io  
Pinned commit: `d7cf1ede44e78c2219e8f12f573024b2915f65c6`

Used as compatible-family corroboration for request/response command names and the BLE challenge/response transforms. The captured RAD 700i `A3 -> A2` and `A1 -> A4` pairs match the documented transforms exactly. This source is not used to promote unobserved RAD 700i commands by itself.

## `car-hud-implementation`

**Car-HUD**, by GitHub user [`grabercn`](https://github.com/grabercn)  
Repository: https://github.com/grabercn/Car-HUD  
Seed implementation inspected: https://github.com/grabercn/Car-HUD/blob/a5692f7a0260cc787a0b6cee7db1a908c3255520/src/cobra_service.py

The project reports successfully connecting to a physical Cobra RAD 700i over BLE and subscribing to radar-alert and GPS characteristics. This repository uses that work as provenance for initial protocol observations rather than copying its implementation.

Credited observations seeded from it include alert/GPS UUIDs, reported read/notify behavior, observed GATT handles, alert mappings, and candidate GPS parsing.

## `cobra-product-page`

Cobra RAD 700i official product page: https://www.cobra.com/products/rad700i

Used only for vendor-confirmed product context such as RAD 700i Bluetooth and Drive Smarter support.

## Adding sources

Prefer stable permalinks/commit hashes for code. For experiments or captures, add a source entry to `protocol.yaml` and link the corresponding sanitized file under `captures/`.
