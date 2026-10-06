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

Drive Smarter sent multiple `82 <setting-id>` requests and received `8B ...` supported-values/information responses plus `8A <setting-id> <current-value>` responses. This confirms that the settings-query family is active on the RAD 700i, but individual setting meanings should only be promoted after one-setting-at-a-time controlled captures.

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



### Candidate Status-embedded alert tail

Compatible-family `RadarResponse` research documents Status (`0x99`) examples where the first status byte is followed by `0xA9` and additional alert bytes. The RAD 700i has directly produced the one-byte Status payloads `0x03` and `0x0B`, but this repository has not yet captured a longer RAD 700i Status frame during an active alert.

The toolbox therefore retains any Status bytes after the first byte and labels a tail beginning with `0xA9` as a **candidate** embedded front/rear alert record. No field semantics are promoted until a physical RAD 700i active-alert capture confirms the relationship.

## Radar alert characteristic

Known candidate layout:

| Offset | Length | Meaning | Confidence |
|---:|---:|---|---|
| 0 | 1 | Band/event code | `observed` for listed alert values |
| 1 | 1 | Candidate signal strength | `inferred` |
| 2+ | ? | Unknown / not yet documented | `unknown` |

### Byte 0 values

| Value | Candidate meaning | Confidence |
|---:|---|---|
| `0x00` | no active alert / clear | `inferred` |
| `0x01` | X | `observed` |
| `0x02` | K | `observed` |
| `0x04` | Ka | `observed` |
| `0x08` | Laser | `observed` |
| `0x10` | Ka POP | `observed` |
| `0x20` | K POP | `observed` |

All nonzero values are powers of two. That pattern alone is not enough to establish that the byte is a bitfield.

### Byte 1

The seed implementation treats byte 1 as signal strength and caps the application-visible result at `10`. That proves neither that the wire value is limited to 0–10 nor that it is linear.

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


## Compatible-family A9 alert-record research

A 2021 public reverse-engineering thread for an Escort Max 360 independently reports the same F5/A9 family and a five-byte alert record after command `A9`:

```text
F5 06 A9 <frequency-1> <frequency-2> <band> <direction-strength> <unknown>
```

The researcher reports deriving the fields by sniffing the detector/app traffic and injecting values. One example laser frame was `F5 06 A9 00 00 38 5F 20`; another radar example was `F5 06 A9 09 3C 29 3E 00`.

This is **compatible-family evidence, not yet a RAD 700i field-level confirmation**. It is useful because the RAD 700i protocol already exposes detector-to-client `A9` as the compatible-family front/rear alert-response command ID, whose public tables describe five bytes per alert. The next RAD 700i test should capture an actual alert and correlate the detector's displayed band/frequency/strength with those five bytes before promoting any field semantics.


The same public injection table provides candidate lookup structure for two fields:

- **Band byte:** the low five bits fall into four-value groups. In the primary family those groups are reported as X, Ku, K, unknown, Ka, POP, Laser, and Strelka. A second family reports MultaRadar CD, MultaRadar CT, Gatso, VG2, Robot, then unknown groups. Higher bits repeat those families.
- **Direction/strength byte:** values `0x00-0x1F` are reported as no direction, `0x20-0x3F` front, `0x40-0x5F` rear, and `0x60-0x7F` side. Within each 0x20 block, the public table groups low-five-bit values into five strength levels: `00-06`, `07-0C`, `0D-12`, `13-18`, and `19-1F`. The source does not establish direction/strength semantics for values with bit 7 set.

### Candidate frequency reconstruction

Compatible-family framing says packet data bytes use seven bits. Combining the two reported frequency bytes as `f1 | (f2 << 7)` produces plausible known-band values in published samples:

- an X-band example with bytes `2F 52` produces `10543`, directly in the expected X-band MHz range;
- a K-band example with bytes `09 3C` produces raw `7689`; adding one 14-bit wrap (`16384`) yields `24073 MHz`.

The toolbox therefore displays the following **hypothesis only** for controlled correlation: X = raw 14-bit value, K = raw + `0x4000`, Ka = raw + `0x8000`. This is not yet a RAD 700i-confirmed frequency formula.

The same thread also documents compatible-family `0x83` setting-change packets. Those writes are intentionally **not** exposed by the toolbox; read-only `0x82` settings discovery is used instead.


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
| `F5 01 AF` | `F5 02 AB 00` | unknown | pair repeated in multiple sessions |
| `F5 02 D1 00` | no deterministic response isolated | unknown | request observed |

The mask bytes are published raw. Individual band/marker bit meanings are not inferred from this capture.

### Setting IDs directly queried by Drive Smarter

The tested RAD 700i was queried with `0x82` for:

```text
01 02 07 0A 0E 10 13 14 15 16 24 25 26 28 29 2B 2C
```

This is significant because IDs `24–2C` are outside the older compatible-family setting table ending at `0x1B`. The toolbox therefore restricts its live Settings Explorer to the IDs that were actually observed and treats old setting names only as hints.

Exact `8B` metadata/current `8A` values are preserved in the sanitized capture summary. IDs `13` and `14` returned `14 A0 05`, matching the older family convention for a numeric range of 20–160 in steps of 5. The range interpretation is corroborated, but the RAD 700i user-facing setting name still requires controlled correlation.

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

The app's parser has explicit branches for `0x82` and `0xA9` that produce alert collections. This materially strengthens the conclusion that these are two distinct alert response forms in the current Drive Smarter protocol family. It still does not establish the RAD 700i field-level A9 payload semantics; physical correlation or further static parser reduction is required.

See [`analysis/2026-10-05-drive-smarter-4.12.0.0.md`](analysis/2026-10-05-drive-smarter-4.12.0.0.md) for the full derived response table and provenance.
