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
- exact current/supported band-enable and marker-enable query/response traffic
- exact RAD 700i setting IDs and numeric values queried by Drive Smarter
- observed unknown request families retained without speculative naming

## `toolbox-observations-2026-09-29`

Sanitized evidence summary: [`captures/2026-09-29-toolbox-observations.md`](captures/2026-09-29-toolbox-observations.md)

This evidence comes from an authenticated RAD 700i toolbox session on physical hardware. Only protocol-relevant packet bytes and visible/audible outcomes are published. No Bluetooth addresses, account data, location data, or system-wide snoop traffic are included.

Direct observations include Tone 1/2 audible output, Tone 0 no audible output, visible posted-speed-limit updates through `A9`, no visible current-speed override from `AA` in the stationary test, no visible display-message result from the compatible-family `9A/09 + ASCII` form, and recurring detector frames `F5 01 82`, `F5 01 A7`, and `F5 02 99 0B`.

## `teslacanalyzer-compatible-protocol`

Repository: https://github.com/BluedDot-IT/TeslaCANalyzer-Controller  
Pinned commit: `870513e99583c24c637d280c21b1b9dc2f9dc5c6`

Used as independent compatible-family corroboration for the `0x9A` display-message construction, `0x9B` tone request, `0xA7` overspeed request handling, and display-location packet research. It does not by itself promote a command to RAD 700i-confirmed status.

## `esclib-compatible-protocol`

Repository: https://github.com/qoq/esclib.github.io  
Pinned commit: `d7cf1ede44e78c2219e8f12f573024b2915f65c6`

Used as compatible-family corroboration for request/response command names and the BLE challenge/response transforms. The captured RAD 700i `A3 -> A2` and `A1 -> A4` pairs match the documented transforms exactly. This source is not used to promote unobserved RAD 700i commands by itself.

## `max360-serial-research`

Public reverse-engineering discussion: https://forum.arduino.cc/t/compare-hex-values-received-via-serial/902323

A researcher working with an Escort Max 360 reports sniffing and injecting the F5 traffic and publishes an `A9` five-byte alert record interpretation (two frequency bytes, band byte, direction/strength byte, final unknown byte) plus compatible-family setting-change examples. This is used only as candidate field-layout evidence for future RAD 700i alert captures; it is not treated as direct RAD 700i evidence.

## `car-hud-implementation`

**Car-HUD**, by GitHub user [`grabercn`](https://github.com/grabercn)  
Repository: https://github.com/grabercn/Car-HUD  
Seed implementation inspected: https://github.com/grabercn/Car-HUD/blob/a5692f7a0260cc787a0b6cee7db1a908c3255520/src/cobra_service.py

The project reports successfully connecting to a physical Cobra RAD 700i over BLE and subscribing to radar-alert and GPS characteristics. This repository uses that work as provenance for initial protocol observations rather than copying its implementation.

Credited observations seeded from it include alert/GPS UUIDs, reported read/notify behavior, observed GATT handles, alert mappings, and candidate GPS parsing.

## `cobra-product-page`

Cobra RAD 700i official product page: https://www.cobra.com/products/rad700i

Used only for vendor-confirmed product context such as RAD 700i Bluetooth and Drive Smarter support.

## `cobra-rad700i-support`

Cobra RAD 700i support/manual page: https://support.cobra.com/support/solutions/articles/47001286267-cobra-rad700i

Used for model-specific behavior and settings context, including the detector's built-in GPS behavior, posted speed-limit display when connected to Drive Smarter, user-facing sensitivity modes, audio features, and documented menu settings. This source does not assign protocol setting IDs.

## `cobra-detector-configuration`

Cobra detector configuration guide: https://support.cobra.com/support/solutions/articles/47001287181-how-should-i-configure-my-cobra-radar-detector-

Used for model-specific RAD 700i sensitivity/detection behavior and built-in-GPS Auto mode. This is product behavior evidence, not packet-level evidence.

## Adding sources

Prefer stable permalinks/commit hashes for code. For experiments or captures, add a source entry to `protocol.yaml` and link the corresponding sanitized file under `captures/`.
