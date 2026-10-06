# Sources and provenance

## Drive Smarter Android inspection target — 2026-10-05

Installed package: `com.cedarelectronics.smartsight`  
Version name: `4.12.0.0`  
Version code: `614`  
Minimum SDK: `28`  
Target SDK: `36`

APK components and SHA-256:

| Component | SHA-256 |
|---|---|
| `base.apk` | `6951b46b91c875a5fdb295839c1e21459728a98eb235f70cadc5651d444e6395` |
| `split_config.arm64_v8a.apk` | `111cc0aeb153ec6453e4364f043813018ded1d86c06e3b1daf894889417ef2bf` |
| `split_config.xxhdpi.apk` | `3ac70be349b239a34a6d9a2b39b651a8a022b427ec0349614a883d18e8aff8d4` |

These hashes identify the exact publicly distributed Android build used for static protocol research. The APKs and decompiled application source are **not** committed to this repository. Any protocol findings derived from inspection must be documented as behavior/structure, with independent physical-capture validation where possible, rather than copying proprietary implementation code.

On 2026-10-06 the same build was re-verified from user-supplied copies of all three APK components and full JADX output. All three APK SHA-256 values matched the table above exactly. This deeper pass therefore refines the existing 4.12.0.0/build-614 evidence target rather than introducing a second build. It reduced marker-enable bits, radar-option IDs and parser structure, display-location packing, turn-by-turn framing/UUIDs, and additional setting-value semantics. The supplied APKs/decompiled sources remain outside this repository.

A broad string inspection of the matching ARM64 split did not reveal an obvious alternate native Cobra/Escort command table. This is a negative search result only and is not treated as proof that native code can never participate in detector-related behavior.

### Static-analysis findings from Drive Smarter 4.12.0.0

JADX output for the exact build above contains a Bluetooth UUID model class under the app's bundled `smartsight.core.bt` code. Its symbolic names distinguish:

- Cobra/iRadar primary service `2A668FA4-2902-4468-8568-3EBE69A930A0`;
- Escort-family service `B5E22DE9-31EE-42AB-BE6A-9BE0837AA344`;
- Escort-family live TX characteristic `B5E22DEA-31EE-42AB-BE6A-9BE0837AA344`;
- Escort-family live RX characteristic `B5E22DEB-31EE-42AB-BE6A-9BE0837AA344`;
- Cedar turn-by-turn service `52AFFC3A-6424-11EC-90D6-0242AC120003`, TX `B5E22DFB-31EE-42AB-BE6A-9BE0837AA344`, and RX `B5E22DFC-31EE-42AB-BE6A-9BE0837AA344` as application-family static evidence.

This is static-analysis corroboration for the UUIDs already observed/corroborated elsewhere; it does not replace physical RAD 700i capture evidence.

The same decompilation exposes typed radar-domain symbols including `RadarMarkerEnable.Type`. A centralized response-code class preserves symbolic names and numeric byte values for the current Drive Smarter protocol family, including `ALERT_RESPONSE (0x82)`, `ALERT_RESPONSE_FRONT_REAR (0xA9)`, `BAND_DIRECTION_RESPONSE (0xAA)`, settings/band/marker/status responses, Bluetooth unlock messages, radar-options responses, and `UNSUPPORTED_REQUEST (0xF0)`.

The current alert-domain object was also reduced far enough to derive the application's exact 4-byte/5-byte alert-record bit extraction for band ID, frequency integer, front/rear signal strength, numeric direction, Laser subtype, and lockout state. The current band/marker models provide byte-index/mask mappings; radar-option enums/parsers, display-location packing, and the separate turn-by-turn transport are also reduced. These derived semantics are recorded in [`analysis/2026-10-05-drive-smarter-4.12.0.0.md`](analysis/2026-10-05-drive-smarter-4.12.0.0.md). They are current-application evidence; commands or alert forms are only promoted to RAD 700i-observed status when backed by physical capture/experiment evidence.


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

## `roadsage-compatible-protocol`

Repository: https://github.com/koiosdigital/RoadSage  
Pinned commit: `6624f44ea38fcc47cbdadf3c58f942729edb13f3`

RoadSage independently carries the compatible-family B5E22DE9/DEA/DEB BLE UUIDs, the F5 command table, speed-limit writes, tone writes, and a five-byte `DISPLAY_LOCATION (0xAD)` packer. The location packer combines alert type, distance, heading, age, and a database flag into seven-bit-safe fields. This is valuable candidate research for future RAD 700i community/location alert work, but it is not promoted as RAD 700i behavior without a physical capture.

## `adwatch-cobra-fingerprint`

Documentation: https://github.com/bensmith83/adwatch/blob/7f35567eec5d2508a946484ea664881e6f98c8fb/docs/protocols/cobra.md

Adwatch independently identifies Cobra RAD/SC products using primary service UUID `2A668FA4-2902-4468-8568-3EBE69A930A0` plus model-name heuristics. This supports the broader Cobra-family BLE fingerprint but does not provide packet-level RAD 700i semantics.

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
