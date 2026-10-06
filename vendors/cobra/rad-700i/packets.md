# Packet notes

This file expands on `protocol.yaml`. It deliberately labels uncertain decoding rather than converting implementation assumptions into protocol facts.

## F5 companion protocol

A 2026-09-11 Android HCI snoop capture of Drive Smarter connected to a physical RAD 700i directly confirms the framing:

```text
F5 <command-plus-payload-length> <command> [payload]
```

The second byte counts the command byte plus payload bytes. Example: `F5 01 94` is a three-byte Status request with no payload.

### Initial client authentication

Observed normal Drive Smarter sequence:

```text
client -> detector  F5 0B A3 <10-byte challenge>
detector -> client  F5 0B A2 <10-byte response>
client -> detector  F5 02 A5 00
client -> detector  F5 01 94
detector -> client  F5 02 99 03
```

Two different sessions showed the same command ordering with different challenge bytes.

The captured `A3 -> A2` pairs exactly match the compatible-family BLE smartphone-key 35-round XTEA-derived transform documented by `qoq/esclib.github.io`. This establishes that the RAD 700i uses the same transform for this direction on the tested firmware.

### Detector-originated authentication challenge

Later in the connected session the detector issued:

```text
detector -> client  F5 0B A1 <10-byte challenge>
client -> detector  F5 0B A4 <10-byte response>
detector -> client  F5 02 A3 00
```

The captured `A1 -> A4` pairs exactly match the compatible-family BLE smartcord-key transform.

### Query/response traffic observed

| Client request | Detector response | Observation |
|---|---|---|
| `F5 01 94` | `F5 02 99 03` | Status |
| `F5 01 91` | `F5 0B 95 03 52 41 44 20 37 30 30 69 00` | Model payload contains `RAD 700i` |
| `F5 01 97` | `F5 02 81 01` | GPS-equipped query |
| `F5 01 89` | `F5 0B 92 40 4D 31 2E 32 2E 33 2E 36 00` | Version payload contains `M1.2.3.6` |
| `F5 01 AC` | `F5 02 A8 07` | Display-capabilities response |
| `F5 01 99` | `F5 02 85 0A` | Display-length response value `10` |

Compatible-family request/response tables corroborate the command names. The bytes/directions above are directly observed on a RAD 700i.

### Speed-related writes observed

Drive Smarter repeatedly sent:

```text
F5 03 A9 19 00
F5 03 AA 00 00
F5 02 AB 00
```

Compatible-family tables identify `A9` as speed-limit update, `AA` as actual-speed update, and `AB` as overspeed-limit data. The A9/AA payload is represented as two 7-bit chunks by the compatible-family implementation. Exact mph/km/h presentation was not independently varied in this capture, so unit/display semantics remain conservative.

### Settings synchronization observed

Drive Smarter sent multiple `82 <setting-id>` requests and received `8B ...` supported-values/information responses plus `8A <setting-id> <current-value>` responses. This confirms that the settings-query family is active on the RAD 700i. Static analysis of the exact Drive Smarter 4.12 build now resolves the current-app setting names for the observed IDs; detector-returned value semantics remain conservative where they have not been physically correlated.

### Follow-up physical toolbox observations — 2026-09-29

A later authenticated toolbox session on the physical RAD 700i exercised a small set of transient commands and observed normal background RX traffic.

#### Tone request `0x9B`

The toolbox sent the compatible-family one-byte tone selector:

```text
F5 02 9B 00  -> no audible effect observed
F5 02 9B 01  -> audible tone observed
F5 02 9B 02  -> audible tone observed
```

This promotes the RAD 700i use of client request `0x9B` for audible tone generation to directly observed status for selector values `1` and `2`. The semantic names/durations of those selectors remain unknown; the UI should call them Tone 0/1/2 rather than "short"/"long" until isolated.

#### Display message request `0x9A`

The toolbox transmitted the compatible-family display-message form using selector `0x09` followed by printable ASCII. The detector produced no visible display change. This is a negative observation, not proof that the command is unsupported: the selector, required display state, or RAD 700i behavior may differ.

#### Speed updates

A toolbox `A9` posted-speed-limit update visibly changed the detector's posted speed-limit field. This independently validates the command interpretation on the tested RAD 700i. A toolbox `AA` current-speed update produced no visible override of the detector's current-speed display during the stationary test. Because the RAD 700i has built-in GPS, precedence between internal-GPS speed and client-provided `AA` remains unresolved.

#### Periodic detector traffic

The authenticated session repeatedly emitted frames including:

```text
F5 01 82
F5 01 A7
F5 02 99 0B
```

For detector-to-client traffic, compatible-family tables identify `0x82` as Alert Response and `0xA7` as an overspeed-warning/data request. On this RAD 700i, `F5 01 82` has zero payload and was observed while no radar alert was active, so the toolbox should treat it as "no active alerts" rather than an unknown radar signal. The physical `A7` frame has zero payload, which differs from some older compatible-family comments that annotate one data byte. Status value `0x0B` is also directly observed; its bit-level meaning remains unknown.

### Not confirmed

The successful tone test does not establish human-readable names for tone selectors. The display-message experiment did not produce a visible result. No firmware/reset/flash/power/lockout/marked-location operation was intentionally tested.



### Current Drive Smarter alert decoding

Drive Smarter 4.12.0.0's alert-domain object resolves the field extraction for both F5 alert forms.

For `0x82 ALERT_RESPONSE`, each alert record is 4 bytes:

```text
b0 b1 b2 b3
```

For `0xA9 ALERT_RESPONSE_FRONT_REAR`, each record is 5 bytes:

```text
b0 b1 b2 b3 b4
```

Band ID:

```text
band = (b2 & 0x1C) >> 2
if b2 & 0x40:
    band |= 0x08
```

Current Drive Smarter band IDs are:

| ID | Band/type |
|---:|---|
| 0 | X |
| 1 | Ku |
| 2 | K |
| 3 | SWS |
| 4 | Ka |
| 5 | POP |
| 6 | Laser |
| 7 | Strelka |
| 8 | MultaRadar CD |
| 9 | MultaRadar CT |
| 10 | Gatso |
| 11 | VG2 |
| 12 | Robot |

For the normal frequency-bearing bands, the app computes:

```text
frequency = (b0 & 0x7F) | ((b1 & 0x7F) << 7) | ((b2 & 0x03) << 14)
front_strength = b3 & 0x1F
```

For a 5-byte A9 record it additionally computes:

```text
rear_strength = b4 & 0x1F
direction = (((b4 & 0x20) >> 5) << 2) + ((b3 & 0x60) >> 5)
```

The app constant `NO_ARROW_SUPPORTED` is `7`. Human-readable names for the remaining numeric direction codes are not yet promoted.

For Laser:

```text
laser_type = b0 & 0x07
```

The same object derives `lockedOut = (b2 & 0x20) == 0`, then forces it false for Ka and POP.

These formulas are **current Drive Smarter application evidence**. They supersede the earlier toolbox's approximate 1–5 signal-strength grouping and band-specific frequency-wrap heuristic. They are not yet a claim that every field has been physically exercised on the RAD 700i firmware.

### Status tails

Drive Smarter 4.12.0.0 accepts Status frames longer than one payload byte, but constructs its Status object from the first payload byte only. Any remaining bytes should therefore be preserved as raw research data. Older compatible-family reports of an A9-shaped Status tail remain historical/family evidence only and are not promoted by the current toolbox UI.

## GPS characteristic

A public implementation attempts this layout for payloads at least 12 bytes long:

| Offset | Length | Candidate type | Candidate interpretation | Confidence |
|---:|---:|---|---|---|
| 0 | 4 | signed LE int32 | latitude × 1e-7 degrees | `hypothesis` |
| 4 | 4 | signed LE int32 | longitude × 1e-7 degrees | `hypothesis` |
| 8 | 2 | unsigned LE int16 | speed, unit unknown | `hypothesis` |
| 10 | 2 | unsigned LE int16 | heading, unit/scale unknown | `hypothesis` |

The same implementation has a fallback for payloads at least 6 bytes long:

- bytes 0–3: signed LE int32 latitude × `1e-6`
- bytes 4–5: signed LE int16 longitude × `1e-4`

The fallback remains tentative and should not be treated as normative without controlled GPS captures.


## Earlier compatible-family A9 research

Before the Drive Smarter 4.12.0.0 alert object was reduced, public Max 360 research correctly indicated a five-byte A9 record and supplied useful sample packets. The current app now provides stronger evidence for the exact field extraction.

The public sample `F5 06 A9 09 3C 29 3E 00` decodes under the current application logic as band ID 2 (K), frequency integer `24073`, front signal strength `30`, rear signal strength `0`, direction code `1`, and `lockedOut=false`.

The older approximation that grouped signal strength into five bars and treated direction as broad 0x20 ranges is superseded. The older "14-bit value plus 0x4000/0x8000 wrap" frequency model is also superseded: bits 0–1 of the band/flags byte supply frequency bits 14–15 directly.

The independent compatible-family work remains useful corroboration and historical provenance, but the toolbox now follows the current Drive Smarter decoder.

## RAD 700i settings-mapping strategy

Cobra's RAD 700i documentation gives a model-specific settings surface that does not exactly match the older compatible-family setting-name table. Documented RAD 700i user settings include Detail (More/Less), Quiet Drive, Auto Mute, Voice, Language, display color, Screen Saver, Smart Power, and Display Car Voltage; the detector also exposes alert/band settings separately.

Because the physical Drive Smarter capture proves that the RAD 700i uses `82 <setting-id>` requests with `8A/8B` responses, those requests can be used to inventory numeric IDs and supported values without changing detector state. The compatible-family ID/name table is useful as a comparison aid, but **must not be copied as the RAD 700i mapping without controlled correlation**.

The recommended mapping procedure is:

1. read all supported IDs through `0x82` only;
2. record the detector's current menu values without changing them;
3. identify obvious cardinality/default matches only as hypotheses;
4. where needed, perform a later one-setting-at-a-time Drive Smarter capture;
5. promote an ID/name/value mapping only after the physical value transition is isolated.

State-changing `0x83` writes remain outside the normal toolbox during this phase.


## Additional read-only inventory recovered from the baseline capture

A 2026-09-29 reanalysis of the original sanitized RAD 700i Drive Smarter HCI capture recovered additional exact request/response families.

| Client request | Detector response | Compatible-family interpretation | RAD 700i evidence |
|---|---|---|---|
| `F5 01 8C` | `F5 06 8F 27 00 00 00 06` | supported band-enable mask | exact bytes observed |
| `F5 01 86` | `F5 06 8C 27 00 00 00 06` | current band-enable mask | exact bytes observed |
| `F5 01 95` | `F5 03 9B 0B 00` | supported marker-enable mask | exact bytes observed |
| `F5 01 92` | `F5 03 97 1B 00` | current marker-enable mask | exact bytes observed |
| `F5 02 84 00` | no uniquely paired response isolated | settings request | request observed |
| `F5 01 AF` | `F5 02 AB 00` | radar enable/disable support query | exact pair observed; current app detector-request table confirms zero-payload query |
| `F5 02 D1 00` | no deterministic response isolated | get all radar options | request observed; current app constructs `D1 + RadarOption.ALL`, establishing `ALL=00` |

The marker masks remain published raw. For band masks, Drive Smarter 4.12.0.0 static analysis now supplies a current byte-index/mask table. Applying that table to the physically observed `27 00 00 00 06` current/supported RAD 700i mask yields set fields for X Band, K Band, Ka Band Superwide, Laser, MultaRadar CD, and MultaRadar CT. Fields at byte index 5 are unavailable because the RAD 700i response contains only five mask bytes. Multi-bit fields are preserved as numeric masks rather than reduced to guessed boolean semantics.

### Setting IDs directly queried by Drive Smarter

The tested RAD 700i was queried with `0x82` for:

```text
01 02 07 0A 0E 10 13 14 15 16 24 25 26 28 29 2B 2C
```

IDs `24–2C` extend beyond the older public compatible-family table, but the current Drive Smarter 4.12 `RadarSetting.Type` sequence resolves the symbolic names used by this app build. For the physically queried high IDs: `24 Detail`, `25 Screen saver`, `26 Smart power`, `28 Low voltage alert`, `29 Quiet drive`, `2B K low band enable`, and `2C Caution area`. The toolbox remains restricted to IDs physically queried on the RAD 700i.

Exact `8B` metadata/current `8A` values are preserved in the sanitized capture summary. IDs `13 Cruise alert` and `14 Over speed alert` returned `14 A0 05`, matching the family convention for a numeric range of 20–160 in steps of 5. The setting names are current-app static evidence; individual value labels remain separately confidence-scoped.

### Safety consequence

Read-only characterization can now replay only the exact observed inventory requests above. State-changing siblings—`83` setting change, `85` band-enable set, `93` marker-enable set, defaults, lockout, power, flash, firmware, and reset operations—remain outside the toolbox research path.


## Candidate display-location packing

RoadSage implements the compatible-family client request `DISPLAY_LOCATION (0xAD)` with a five-byte payload. Its packing logic uses seven-bit-safe fields containing:

- alert/location type;
- distance split across multiple bytes;
- heading represented at half-degree resolution;
- an age field;
- a database/source flag.

The exact bit packing is available in the pinned RoadSage source, but this repository does **not** yet claim that the RAD 700i accepts the same layout. Cobra's own product documentation confirms that Drive Smarter can surface community/location alerts on connected detectors, so this is a high-value capture target rather than a write we should guess.

Toolbox policy: keep `0xAD` blocked until a physical RAD 700i Drive Smarter capture exercises it or an equivalently strong controlled observation confirms the payload.


## Drive Smarter 4.12.0.0 static response map

Static inspection of the exact hashed Android build documented in `sources.md` reveals a centralized radar response-code table. It independently names the currently implemented family responses, including `0x82 ALERT_RESPONSE`, `0xA9 ALERT_RESPONSE_FRONT_REAR`, `0xAA BAND_DIRECTION_RESPONSE`, `0xAB RADAR_ENABLE_DISABLE_SUPPORT_RESPONSE`, `0xAC RADAR_OPTIONS_RESPONSE`, and `0xAE RADAR_OPTIONS_INFO_RESPONSE`, alongside the settings/band/marker/status/authentication responses already seen in compatible-family research.

The app's parser has explicit branches for `0x82` and `0xA9` and the alert-domain object has been reduced to the exact field operations documented above. The remaining gap is model-level physical correlation of a non-empty RAD 700i alert, not application-side field decoding.

See [`analysis/2026-10-05-drive-smarter-4.12.0.0.md`](analysis/2026-10-05-drive-smarter-4.12.0.0.md) for the full derived response table and provenance.


### Current Drive Smarter request enum

Static analysis of Drive Smarter 4.12.0.0 now provides the exact current request-command symbols for the major radar protocol operations. Of particular relevance to the RAD 700i capture:

- `0xAF = DISABLE_ENABLE_RADAR` in the request enum, while the detector-query table stores exact `F5 01 AF` as `RADAR_ENABLE_DISABLE_REQUEST`; its paired response is `0xAB RADAR_ENABLE_DISABLE_SUPPORT_RESPONSE`. The toolbox permits only this observed zero-payload read/support query.
- `0xD1 = RADAR_OPTIONS_REQUEST`; the app's `getRadarOptions` path sends `D1` plus `RadarOption.ALL`. The physical `D1 00` capture therefore establishes `ALL=0x00`. The toolbox permits only this exact read-like form; `D0` writes and unobserved per-option `D3` queries remain blocked.
- `0xAD = DISPLAY_LOCATION` and `0xAE = DISPLAY_CLEAR_LOCATION`, strengthening the current-app relevance of location/community display research.
- `0xD0 = RADAR_OPTIONS_SET` and `0xD3 = RADAR_OPTIONS_INFORMATION`.
- the current enum does not expose the older compatible-family arbitrary `DISPLAY_MESSAGE 0x9A` or `PLAY_TONE 0x9B` request symbols.

No new state-changing request is enabled in the toolbox from static analysis alone.

### Current Drive Smarter alert record widths

Drive Smarter 4.12.0.0 parses:

- detector `0x82 ALERT_RESPONSE` as zero or more **4-byte records**;
- detector `0xA9 ALERT_RESPONSE_FRONT_REAR` as zero or more **5-byte records**.

The alert-domain object has now also been reduced: exact band extraction, frequency assembly, signal-strength masks, rear-strength handling, numeric direction extraction, Laser subtype handling, and lockout flag behavior are documented above. Physical RAD 700i correlation is still required before claiming that every app-family field is exercised by this model.

### Drive Smarter alert selection behavior

After decoding complete 4-byte or 5-byte records, the current app skips SWS records, accepts Laser without an ordinary frequency, accepts other bands only when the reconstructed frequency is greater than zero, and stops after the first qualifying record. Research tooling should preserve all raw complete records and expose this app-visible subset separately.

### Status parser note

Drive Smarter 4.12.0.0 accepts Status frames with at least one payload byte but constructs its status object from only the first payload byte. Older compatible-family research describing an embedded A9 tail is therefore retained only as historical/family evidence, not as preferred current-app behavior.
