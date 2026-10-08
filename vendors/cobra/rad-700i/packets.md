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

Current Drive Smarter 4.12 confirms `A9` as posted speed-limit update, `AA` as actual-speed update, and `AB` as overspeed-limit data. A9/AA use the protocol's two 7-bit chunks. The app's overspeed preference path also resolves the observed `AB 00`: OFF is represented internally as `-1` and produces payload `00`; otherwise Drive Smarter derives the threshold in the active unit mode, adds 64, and sends that byte. Exact physical presentation for every nonzero AB value has not been varied on the RAD 700i.

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

The baseline Drive Smarter session also directly captured detector `F5 02 A6 03`. Static analysis of this exact app build shows that A6 is a bitmask: bit 0 requests posted speed-limit data and bit 1 requests actual-speed data. Drive Smarter stores only `payload & 0x03`; therefore the physically observed value `03` requests both streams.


For detector-to-client traffic, `0x82` is Alert Response and `0xA7` is the overspeed-warning request. On this RAD 700i, `F5 01 82` has zero payload and was observed while no radar alert was active, so the toolbox treats it as "no active alerts" rather than an unknown radar signal. The physical `A7` frame has zero payload. Current Drive Smarter starts a repeating four-second AB overspeed-update job when A7 is received.

Current Drive Smarter resolves the known Status bits as:

- `0x01` detector communicating;
- `0x02` detector powered;
- `0x04` detector muted.

The physical `0x03` status is therefore communicating + powered, with mute clear. The physical `0x0B` status is communicating + powered + unresolved bit `0x08`, with mute clear. Bits `0x08` and above remain raw until independently reduced.

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

The fallback remains tentative and should not be treated as normative without controlled GPS captures. The exact Drive Smarter 4.12 managed decompilation and split-APK string scan do not contain the `FE51` UUID literal, so this endpoint/layout remains sourced from the independent public implementation rather than from the current Drive Smarter build.


## Earlier compatible-family A9 research

Before the Drive Smarter 4.12.0.0 alert object was reduced, public Max 360 research correctly indicated a five-byte A9 record and supplied useful sample packets. The current app now provides stronger evidence for the exact field extraction.

The public sample `F5 06 A9 09 3C 29 3E 00` decodes under the current application logic as band ID 2 (K), frequency integer `24073`, front signal strength `30`, rear signal strength `0`, direction code `1`, and `lockedOut=false`.

The older approximation that grouped signal strength into five bars and treated direction as broad 0x20 ranges is superseded. The older "14-bit value plus 0x4000/0x8000 wrap" frequency model is also superseded: bits 0–1 of the band/flags byte supply frequency bits 14–15 directly.

The independent compatible-family work remains useful corroboration and historical provenance, but the toolbox now follows the current Drive Smarter decoder.

## RAD 700i settings mapping

The physical Drive Smarter capture proves that the RAD 700i uses `82 <setting-id>` requests with `8A/8B` responses. The exact Drive Smarter 4.12 setting enum now resolves request IDs through `0x2C`, and the current app resource/range tables resolve value labels where this build actually defines them.

Evidence is kept split by layer:

1. **physical RAD 700i evidence:** which setting IDs and numeric values were actually queried/returned;
2. **current-app static evidence:** symbolic setting names, resource-backed value labels, and range construction;
3. **still unresolved:** values absent from the app mapping, most notably physical Sensitivity value `0x10`, plus any desired independent one-setting-at-a-time validation.

The current app's resource-label map is broader than its dedicated `0x8B` metadata-handler map. A label can therefore be exact current-app UI semantics without proving that this build actively queries metadata for that setting. State-changing `0x83` writes remain outside the normal toolbox.


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

Drive Smarter 4.12.0.0 now supplies exact maps for both band and marker masks. Applying the marker map to physical RAD 700i evidence resolves `0B 00` supported markers as Red Light Camera, Speed Camera, and Speed Trap; `1B 00` current markers adds Other. Applying the band map to the physically observed `27 00 00 00 06` current/supported RAD 700i mask yields set fields for X Band, K Band, Ka Band Superwide, Laser, MultaRadar CD, and MultaRadar CT. Fields at byte index 5 are unavailable because the RAD 700i response contains only five mask bytes. Multi-bit band fields are preserved as numeric masks rather than reduced to guessed boolean semantics.

### Setting IDs directly queried by Drive Smarter

The tested RAD 700i was queried with `0x82` for:

```text
01 02 07 0A 0E 10 13 14 15 16 24 25 26 28 29 2B 2C
```

IDs `24–2C` extend beyond the older public compatible-family table, but the current Drive Smarter 4.12 `RadarSetting.Type` sequence resolves the symbolic names used by this app build. For the physically queried high IDs: `24 Detail`, `25 Screen saver`, `26 Smart power`, `28 Low voltage alert`, `29 Quiet drive`, `2B K low band enable`, and `2C Caution area`. The toolbox remains restricted to IDs physically queried on the RAD 700i.

Exact `8B` metadata/current `8A` values are preserved in the sanitized capture summary. The current Drive Smarter 4.12 resource tables and parser now also resolve most of the returned list values: for example Brightness `00/01/02/03 = Full dark/Minimum/Medium/Maximum`, Units `00/01 = Imperial/Metric`, Detail `00/01 = Less/More`, and Screen Saver `00/01/03 = Off/1 Minute/3 Minute`. Display Color's physical supported sequence `07 02 03 01 06` maps to White, Green, Blue, Red, Yellow. The high-ID toggles Smart Power, Low Voltage Alert, Quiet Drive, K Low Band Enable, and Caution Area use Off/On labels in the current app.

IDs `13 Cruise alert` and `14 Over speed alert` returned `14 A0 05`; the current parser explicitly builds Off plus a numeric range of 20–160 in steps of 5. One anomaly remains intentionally unresolved: Sensitivity returned supported bytes `00 07 08 09 10` and current value `10`. The current app label table maps 0=Auto, 7=Low, 8=Medium, and 9=High, but has no index 16 (`0x10`), so the detector's `0x10` value is not assigned a guessed name.

### Safety consequence

Read-only characterization can now replay only the exact observed inventory requests above. State-changing siblings—`83` setting change, `85` band-enable set, `93` marker-enable set, defaults, lockout, power, flash, firmware, and reset operations—remain outside the toolbox research path.

### Current-app state-changing/control packet shapes

Static analysis of Drive Smarter 4.12 resolves these exact client packet shapes:

```text
LOCK active alert       F5 01 80
UNLOCK active alert     F5 01 81
SETTING_CHANGE          F5 03 83 <setting-id> <value>
BAND_ENABLES_SET        F5 <mask-length+1> 85 <mask bytes...>
MARKER_ENABLES_SET      F5 03 93 <mask-byte-0> <mask-byte-1>
MUTE false              F5 02 9E 00
MUTE true               F5 02 9E 01
RADAR_OPTIONS_SET       F5 03 D0 <option-id> <value>
```

These are **current-application static semantics**, not authorization to transmit them. The toolbox keeps all persistent/state-changing forms blocked. Lock/unlock/mute are also kept blocked until deliberately isolated on physical RAD 700i hardware.

Drive Smarter accepts one-byte detector `0x84 LOCK_RESPONSE` and `0x86 UNLOCK_RESPONSE` frames when their result byte is anything other than `0x01`; `0x01` is the explicit error value in the current parser.



## Current Drive Smarter alert/location IDs

Drive Smarter passes each alert object's `markedLocationId` into the first logical field of `DISPLAY_LOCATION`.

| Type | ID |
|---|---:|
| Speed Trap (Defender) | 1 |
| Speed Camera (Defender) | 2 |
| Red Light Camera | 3 |
| Red Light & Speed Camera | 7 |
| Average Speed Camera | 8 |
| Air Patrol | 10 |
| X | 128 |
| Ku | 129 |
| K | 130 |
| Ka | 131 |
| POP | 132 |
| Laser | 133 |
| Stationary Police | 134 |
| Mobile Camera | 135 |
| Strelka | 136 |
| MultaRadar CD | 137 |
| MultaRadar CT | 138 |
| Gatso | 139 |
| Speed Camera (Scout) | 141 |
| Moving Police | 142 |
| Accident | 143 |
| Detour | 144 |
| Work Zone | 145 |
| Road Hazard | 146 |
| Traffic Jam | 147 |
| VG2 | 148 |
| Robot | 149 |
| Gatso RT4 | 150 |
| Mesta 210c | 151 |
| Mesta Fusion | 152 |
| Dahua | 153 |

Average Speed Camera overrides its base ID with `5` for START and `6` for END. Air Patrol uses `9` for START and `11` for END. HOV Lane Camera and SWS expose `-1` rather than a normal positive marked-location ID.

Drive Smarter maps alert threat level YELLOW/ORANGE/RED to protocol level `0/1/2`, reporter USER/DATABASE to `0/1`, and normalizes a negative heading by adding 360 before the five-byte display-location packer.

These values are exact current-app semantics. Physical RAD 700i rendering of the location/community alert family is still unvalidated.

## Current Drive Smarter display-location packing

The exact Drive Smarter 4.12 implementation now removes the earlier dependency on a compatible-family guess. When its display-location capability flag is set, the app emits `DISPLAY_LOCATION (0xAD)` with five seven-bit-safe payload bytes.

Logical inputs are:

- 8-bit threat/location type;
- distance in feet;
- 2-bit level;
- heading in degrees;
- 1-bit database/source flag.

Drive Smarter divides heading by two with integer division and packs:

```text
h = (headingDegrees / 2) & 0xFF
p0 = threatType & 0x7F
p1 = (((threatType & 0x80) >> 7) | (distanceFeet << 1)) & 0x7F
p2 = (distanceFeet >> 6) & 0x7F
p3 = ((distanceFeet >> 13) | (h << 3)) & 0x7F
p4 = (((level & 0x03) << 5) | (h >> 4) | ((database & 0x01) << 4)) & 0x7F
```

The transmitted frame is:

```text
F5 06 AD p0 p1 p2 p3 p4
```

The app sends zero-payload `F5 01 AE` for `DISPLAY_CLEAR_LOCATION`.

Drive Smarter itself tests display-capability bit `0x04` before using these calls. The physical RAD 700i returned capability byte `0x07`, so this build marks display-location support true for that session. This is still **not** a physical proof of what the RAD 700i renders. The toolbox keeps both writes blocked until one controlled hardware observation or Drive Smarter capture validates the visible behavior.


## Radar-options structure

The exact current-app radar-option surface is:

| ID | Option |
|---:|---|
| `00` | ALL request selector |
| `01` | X Filter |
| `02` | K Filter |
| `03` | K Notch |
| `04` | Wi-Fi Filter |
| `05` | K Notch 2 |
| `06` | Ka Notch |

Concrete option values are shared across all six options:

| Value | Meaning |
|---:|---|
| `00` | Off |
| `01` | On |
| `02` | Low |
| `03` | Medium |
| `04` | High |

Drive Smarter parses detector `0xAC` responses as repeated two-byte `<option-id> <value>` records beginning immediately after the F5 command. It parses `0xAE` option-info responses as:

```text
<option-id> <info-type> [info-values...]
```

where info type `0` is LIST and `1` is NUMBER. LIST values use the same Off/On/Low/Medium/High enum. The inspected NUMBER path does not reduce the remaining bytes further, so they stay raw.

Drive Smarter requests all options with the physically observed `F5 02 D1 00`. After a response, the app can send `D3 <option-id>` for concrete options whose metadata is missing. The toolbox decodes `AC/AE` passively but continues to block `D3` because no physical RAD 700i D3/AE exchange has been isolated.

## Current-app marker-enable bit map

The marker state is two bytes:

| Byte | Mask | Marker |
|---:|---:|---|
| 0 | `01` | Red Light Camera |
| 0 | `02` | Speed Camera |
| 0 | `04` | Average Speed Camera |
| 0 | `08` | Speed Trap |
| 0 | `10` | Other |
| 0 | `20` | Camera |
| 0 | `40` | Strelka |
| 1 | `01` | Red Light & Speed Camera |
| 1 | `02` | School Zone |
| 1 | `04` | HOV Lane Camera |
| 1 | `08` | Railway Camera |
| 1 | `10` | Accident Blackspot |
| 1 | `20` | Air Patrol |

The app's state-changing marker writer is `F5 03 93 <byte0> <byte1>`. That fact is documented but the write remains outside the normal toolbox.

## Current-app turn-by-turn protocol

Drive Smarter contains a separate Cedar turn-by-turn BLE transport:

```text
service  52AFFC3A-6424-11EC-90D6-0242AC120003
TX       B5E22DFB-31EE-42AB-BE6A-9BE0837AA344
RX       B5E22DFC-31EE-42AB-BE6A-9BE0837AA344
```

Unlike radar traffic, turn-by-turn traffic uses an `AA 55` envelope. Static request values are `01` capabilities, `02` supported maneuvers, `03` maneuver data, and `04` cancel, with `BB 66` ending a frame.

The app's capability request is:

```text
AA 55 01 00 01 01 00 BB 66
```

and the supported-maneuver request uses the same shape with command/checksum `02`.

For a command-`01` capability response, the app reads byte 7 as the ETA-support flag, byte 8 as the lane-data-support flag, and byte 9 as maximum road/address text length. A command-`02` response marks maneuver support available.

Maneuver packets include maneuver type/modifier, exit number, distance ×10, distance unit, optional ETA, lane counts, NUL-terminated UTF-8 road text, a 16-bit additive checksum, and `BB 66`. The current maneuver and modifier code tables are documented in the static-analysis note.

This transport has **not** been observed in a physical RAD 700i GATT inventory. It remains static application evidence and is not exposed as a live toolbox writer.

## Typed version reporting and F5 band-direction acknowledgments

Drive Smarter 4.12 parses `0x92 VERSION_RESPONSE` as typed components. The exact RAD 700i payload `40 4D 31 2E 32 2E 33 2E 36 00` has a leading `0x40` MAIN marker without an adjacent version; the `0x4D` SMARTCORD_MAIN marker is followed by `1.2.3.6`. Thus `1.2.3.6` is associated with **SMARTCORD_MAIN** in the current-app parser; it is not independent proof of the radar MAIN processor firmware revision. See the current-app version-type table in the [static analysis](analysis/2026-10-05-drive-smarter-4.12.0.0.md).

`0xAA BAND_DIRECTION_RESPONSE` under the **F5 radar framing** returns a simple OK result in the current Drive Smarter parser and has no decoded direction field. This is different from the numeric direction embedded in some `0xA9` front/rear alert records, and entirely different from the `AA 55` header of the separate turn-by-turn transport. Preserve any physical F5 `0xAA` payload raw; no such RAD 700i capture has yet been established.

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

Drive Smarter 4.12.0.0 accepts Status frames with at least one payload byte but constructs its status object from only the first payload byte. Known bit semantics are communicating=`0x01`, powered=`0x02`, and muted=`0x04`; higher bits remain unresolved. Older compatible-family research describing an embedded A9 tail is therefore retained only as historical/family evidence, not as preferred current-app behavior.
