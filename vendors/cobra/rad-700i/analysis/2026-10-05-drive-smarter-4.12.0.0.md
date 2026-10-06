# Drive Smarter Android 4.12.0.0 static protocol analysis

This note records derived protocol facts from static inspection of the publicly distributed Android application build identified in `sources.md`.

The APK and decompiled source are not distributed by this repository. This note contains only derived protocol names, numeric identifiers, structural observations, and provenance.

## Build identity

- package: `com.cedarelectronics.smartsight`
- version name: `4.12.0.0`
- version code: `614`
- base APK SHA-256: `6951b46b91c875a5fdb295839c1e21459728a98eb235f70cadc5651d444e6395`

## Bluetooth UUID symbols

The application carries symbolic UUID entries for:

- Cobra/iRadar primary service: `2A668FA4-2902-4468-8568-3EBE69A930A0`
- Escort-family service: `B5E22DE9-31EE-42AB-BE6A-9BE0837AA344`
- Escort live TX: `B5E22DEA-31EE-42AB-BE6A-9BE0837AA344`
- Escort live RX: `B5E22DEB-31EE-42AB-BE6A-9BE0837AA344`

## Response command table present in the application

The current application contains a centralized response-code table. Signed Java byte constants convert to the following unsigned wire values:

| Wire value | Application symbol |
|---:|---|
| `0x80` | MUTE_BUTTON_PRESS |
| `0x81` | GPS_EQUIPPED_RESPONSE |
| `0x82` | ALERT_RESPONSE |
| `0x84` | LOCK_RESPONSE |
| `0x85` | DISPLAY_LENGTH_RESPONSE |
| `0x86` | UNLOCK_RESPONSE |
| `0x8A` | SETTINGS_RESPONSE |
| `0x8B` | SETTINGS_INFORMATION_RESPONSE |
| `0x8C` | BAND_ENABLES_RESPONSE |
| `0x8F` | BAND_ENABLES_SUPPORTED_RESPONSE |
| `0x90` | FLASH_ERASE_RESPONSE |
| `0x92` | VERSION_RESPONSE |
| `0x94` | FIRMWARE_UPDATE_STATUS |
| `0x95` | MODEL_INFO_RESPONSE |
| `0x97` | MARKER_ENABLES_RESPONSE |
| `0x99` | STATUS_RESPONSE |
| `0x9B` | MARKER_ENABLES_SUPPORTED_RESPONSE |
| `0x9C` | REPORT_BUTTON_PRESS |
| `0x9D` | MODEL_NUMBER_REQUEST |
| `0xA0` | UPDATE_APPROVAL_REQUEST |
| `0xA1` | BLUETOOTH_PROTOCOL_UNLOCK_REQUEST |
| `0xA2` | BLUETOOTH_PROTOCOL_UNLOCK_RESPONSE |
| `0xA3` | BLUETOOTH_PROTOCOL_UNLOCK_STATUS |
| `0xA4` | BLUETOOTH_CONNECTION_DELAY_RESPONSE |
| `0xA5` | BLUETOOTH_SERIAL_NUMBER_RESPONSE |
| `0xA6` | SPEED_INFORMATION_REQUEST |
| `0xA7` | OVERSPEED_WARNING_REQUEST |
| `0xA8` | DISPLAY_CAPABILITIES_RESPONSE |
| `0xA9` | ALERT_RESPONSE_FRONT_REAR |
| `0xAA` | BAND_DIRECTION_RESPONSE |
| `0xAB` | RADAR_ENABLE_DISABLE_SUPPORT_RESPONSE |
| `0xAC` | RADAR_OPTIONS_RESPONSE |
| `0xAE` | RADAR_OPTIONS_INFO_RESPONSE |
| `0xF0` | UNSUPPORTED_REQUEST |

The application also defines turn-by-turn response values `0x01` and `0x02`.

This table is strong evidence for the protocol family implemented by Drive Smarter 4.12.0.0. It does **not** mean every response above is supported or emitted by the RAD 700i.

## Parser structure

The application's response parser has explicit branches for both `ALERT_RESPONSE (0x82)` and `ALERT_RESPONSE_FRONT_REAR (0xA9)`, and constructs collections for both alert forms. It separately parses band direction, settings, band masks, marker masks, status, speed-information requests, overspeed requests, display capabilities, authentication messages, radar-options messages, and other response families.

The parser treats Status as an object derived from the first payload byte. It expects a one-byte payload for speed-information requests and a one-byte payload for display-capabilities responses. The alert-domain object and parser loop have now also been reduced below, including field extraction and the application's first-qualifying-record selection behavior.

## Request enum evidence

The same build contains a typed `RadarRequest` enum. The request-command portion of that enum maps to:

| Wire value | Application symbol |
|---:|---|
| `0x80` | LOCK_REQUEST |
| `0x81` | UNLOCK_REQUEST |
| `0x82` | SETTINGS_INFORMATION |
| `0x83` | SETTING_CHANGE |
| `0x84` | SETTINGS_REQUEST |
| `0x85` | BAND_ENABLES_SET |
| `0x86` | BAND_ENABLES_REQUEST |
| `0x89` | VERSION_REQUEST |
| `0x8C` | BAND_ENABLES_SUPPORTED |
| `0x91` | MODEL_INFO_REQUEST |
| `0x92` | MARKER_ENABLES_REQUEST |
| `0x93` | MARKER_ENABLES_SET |
| `0x94` | STATUS_REQUEST |
| `0x95` | MARKER_ENABLES_SUPPORTED |
| `0x97` | GPS_EQUIPPED_REQUEST |
| `0x99` | DISPLAY_LENGTH |
| `0x9D` | MODEL_NUMBER_RESPONSE |
| `0x9E` | MUTE |
| `0xA1` | UPDATE_APPROVAL_RESPONSE |
| `0xA3` | BLUETOOTH_PROTOCOL_UNLOCK_REQUEST |
| `0xA4` | BLUETOOTH_PROTOCOL_UNLOCK_RESPONSE |
| `0xA5` | BLUETOOTH_PROTOCOL_UNLOCK_STATUS |
| `0xA9` | SPEED_LIMIT_UPDATE |
| `0xAA` | ACTUAL_SPEED_UPDATE |
| `0xAB` | OVERSPEED_LIMIT_DATA |
| `0xAC` | DISPLAY_CAPABILITIES |
| `0xAD` | DISPLAY_LOCATION |
| `0xAE` | DISPLAY_CLEAR_LOCATION |
| `0xAF` | DISABLE_ENABLE_RADAR |
| `0xD0` | RADAR_OPTIONS_SET |
| `0xD1` | RADAR_OPTIONS_REQUEST |
| `0xD3` | RADAR_OPTIONS_INFORMATION |

The enum also contains turn-by-turn request/subfield values. Those later enum entries reuse small integers for maneuver, modifier, and unit values and must not all be interpreted as top-level radar request opcodes.

Two static-analysis results directly resolve previously unknown physical RAD 700i capture traffic:

- observed client `F5 01 AF` is the exact packet stored by the app's `RADAR_ENABLE_DISABLE_REQUEST` detector-query entry. The paired detector `F5 02 AB 00` is parsed as `RADAR_ENABLE_DISABLE_SUPPORT_RESPONSE` with one value byte. This resolves the observed zero-payload AF form as a read/support query. Payload-bearing or state-changing AF variants are not inferred.
- observed client `F5 02 D1 00` is emitted by the app's `getRadarOptions` path as `RADAR_OPTIONS_REQUEST` plus `RadarOption.ALL`. The physical payload byte therefore establishes `ALL = 0x00` for this build. The exact `D1 00` form is read-like; `D0 RADAR_OPTIONS_SET` remains state-changing and blocked.

Notably, the current Drive Smarter request enum does **not** contain the older compatible-family arbitrary `DISPLAY_MESSAGE (0x9A)` or `PLAY_TONE (0x9B)` request symbols. The physical RAD 700i still responds audibly to tested `0x9B` selectors, but these operations appear to be legacy/family behavior rather than current Drive Smarter 4.12 request-enum features.

## Alert record decoding

Static inspection of the alert-domain object resolves the field extraction used by current Drive Smarter 4.12.0.0.

The response parser still establishes the two record widths:

- `ALERT_RESPONSE (0x82)`: zero or more 4-byte records.
- `ALERT_RESPONSE_FRONT_REAR (0xA9)`: zero or more 5-byte records.

For a record `b0 b1 b2 b3 [b4]`, Drive Smarter derives the band as:

```text
band = (b2 & 0x1C) >> 2
if (b2 & 0x40) != 0:
    band |= 0x08
```

The application constants map those band IDs as:

| Band ID | Application meaning |
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

For X, Ku, K, Ka, POP, Strelka, MultaRadar CD, MultaRadar CT, Gatso, VG2, and Robot, Drive Smarter reconstructs the integer `frequency` as:

```text
frequency =
    (b0 & 0x7F)
  | ((b1 & 0x7F) << 7)
  | ((b2 & 0x03) << 14)
```

This replaces the older compatible-family "14-bit value plus band-specific wrap" hypothesis: the two high frequency bits are carried directly in bits 0–1 of `b2`. The application names the resulting integer `frequency`; unit interpretation should remain separately documented until model-level correlation is available.

For the 4-byte `0x82` record:

```text
front_signal_strength = b3 & 0x1F
signal_direction = 7  # application constant NO_ARROW_SUPPORTED
```

For the 5-byte `0xA9` record:

```text
front_signal_strength = b3 & 0x1F
rear_signal_strength  = b4 & 0x1F
signal_direction =
    (((b4 & 0x20) >> 5) << 2)
  + ((b3 & 0x60) >> 5)
```

The exact human-readable meaning of direction codes other than application constant `7 = NO_ARROW_SUPPORTED` has not yet been extracted, so numeric direction values are preferable to guessed front/rear/side labels.

For Laser (`band == 6`), Drive Smarter instead records:

```text
laser_type = b0 & 0x07
```

and does not populate the ordinary frequency/strength fields in this alert object path. SWS (`band == 3`) likewise does not enter the normal frequency branch.

The application also derives a `lockedOut` flag from `b2`:

```text
lockedOut = (b2 & 0x20) == 0
```

then forces `lockedOut = false` for Ka and POP.

These are current-application decoding semantics, not merely compatible-family guesses. A physical RAD 700i active-alert capture is still needed to establish which of the current app's alert forms/fields this specific firmware emits in practice.

The parser loop adds at most one alert to the collection it returns to the rest of the application. In order, it:

1. skips SWS records (`band == 3`);
2. accepts Laser even without an ordinary frequency;
3. accepts other decoded bands only when `frequency > 0`; and
4. stops after the first qualifying record.

This is application presentation behavior, not a reason to discard later raw records during protocol research. The toolbox therefore preserves every complete raw record and separately exposes the subset Drive Smarter itself would surface.

## Current setting-ID map

Drive Smarter's current `RadarSetting.Type` enum, its `getReqvalue()` keyed handler table, the established low-ID family mapping, and the physically observed RAD 700i IDs align on the one-based request-value sequence below. This resolves the current-app symbolic name for the observed high IDs without claiming that every candidate value label has been physically correlated.

| ID | Drive Smarter setting |
|---:|---|
| `01` | Sensitivity |
| `02` | Brightness |
| `03` | Dark mode |
| `04` | Pilot mode |
| `05` | Power-on sequence |
| `06` | Meter mode |
| `07` | AutoMute |
| `08` | Audio tones |
| `09` | ZR3 / shifter mode |
| `0A` | Voice |
| `0B` | Speed alert |
| `0C` | Auto volume |
| `0D` | Auto power |
| `0E` | Units |
| `0F` | GPS filter |
| `10` | AutoLearn |
| `11` | Alert lamp |
| `12` | Display orientation |
| `13` | Cruise alert |
| `14` | Over speed alert |
| `15` | Language |
| `16` | Display color |
| `17` | Speed on display |
| `18` | Speaker volume |
| `19` | Headset volume |
| `1A` | User mode |
| `1B` | Arrow mode |
| `1C` | Over speed limit alert |
| `1D` | Bluetooth enable |
| `1E` | Wi-Fi enable |
| `1F` | Auto update |
| `20` | Scanning bar |
| `21` | Frequency |
| `22` | Alert ring |
| `23` | Interface mode |
| `24` | Detail |
| `25` | Screen saver |
| `26` | Smart power |
| `27` | Vehicle voltage display |
| `28` | Low voltage alert |
| `29` | Quiet drive |
| `2A` | K notch filter |
| `2B` | K low band enable |
| `2C` | Caution area |

The physical capture directly queried IDs `01 02 07 0A 0E 10 13 14 15 16 24 25 26 28 29 2B 2C`. The names above are current-app static semantics; the detector-returned `8A/8B` values remain raw where their user-facing value meanings have not been isolated.

## Radar-options and radar-support query construction

Current Drive Smarter code constructs these packets:

- `getRadarOptions`: `F5 02 D1 <RadarOption.ALL>`; the physical capture is `F5 02 D1 00`, establishing `ALL = 0x00` for this build.
- `radarOptionSet`: `F5 03 D0 <option> <value>`; this is state-changing.
- `getRadarOptionInfo`: `F5 02 D3 <option>`; this is read-like in current app code but has not been physically observed on the RAD 700i.
- detector support query: exact zero-payload `F5 01 AF`, represented by the app's detector request table and paired physically with `F5 02 AB 00`.

The exact current-app radar-option IDs are:

| ID | RadarOption |
|---:|---|
| `00` | ALL |
| `01` | X_FILTER |
| `02` | K_FILTER |
| `03` | K_NOTCH |
| `04` | WIFI_FILTER |
| `05` | K_NOTCH_2 |
| `06` | KA_NOTCH |

The generic radar-option value enum is:

| Value | Current-app label |
|---:|---|
| `00` | Off |
| `01` | On |
| `02` | Low |
| `03` | Medium |
| `04` | High |

The current app parses `RADAR_OPTIONS_RESPONSE (0xAC)` as repeated `<option-id> <value>` pairs beginning at F5 frame offset 3. It accepts the response only when the total frame length is greater than four bytes, resolves recognized option IDs through the table above, and resolves recognized values through the Off/On/Low/Medium/High enum.

The current app parses `RADAR_OPTIONS_INFO_RESPONSE (0xAE)` with:

- F5 frame offset 3: radar option ID;
- offset 4: info type;
- info type `0 = LIST`;
- info type `1 = NUMBER`;
- for `LIST`, bytes from offset 5 onward are supported values filtered against the option's allowed value enum;
- single-byte value `0xF4` is treated as the unsupported sentinel.

The current parser contains no explicit value-list construction for `NUMBER` in this method. Do not invent numeric-range semantics for that case.

Only `D1 00` has direct RAD 700i request evidence. `D3 <option>` is sufficiently reduced for passive/offline modeling but should remain out of the toolbox's default live inventory until directly observed or otherwise model-validated. `D0` remains blocked because it changes detector state.

## Marker-enable bitfield model

Drive Smarter 4.12.0.0 exposes the exact two-byte marker-enable map:

| Marker | Byte index | Mask |
|---|---:|---:|
| Red Light Camera | 0 | `0x01` |
| Speed Camera | 0 | `0x02` |
| Average Speed Camera | 0 | `0x04` |
| Speed Trap | 0 | `0x08` |
| Other | 0 | `0x10` |
| Camera | 0 | `0x20` |
| Strelka | 0 | `0x40` |
| Red Light & Speed Camera | 1 | `0x01` |
| School Zone | 1 | `0x02` |
| HOV Lane Camera | 1 | `0x04` |
| Railway Camera | 1 | `0x08` |
| Accident Blackspot | 1 | `0x10` |
| Air Patrol | 1 | `0x20` |

The current parser indexes each marker at `frame[3 + byteIndex]` and tests `(value & mask) == mask`. Applying that exact application map to the physical RAD 700i capture:

- supported mask `0B 00`: Red Light Camera, Speed Camera, Speed Trap;
- current mask `1B 00`: Red Light Camera, Speed Camera, Speed Trap, Other.

The bytes are direct physical evidence. Their names/bit positions are current-app static semantics. The apparent current `Other` bit outside the supported mask should be preserved as observed rather than normalized away.

## Display-location encoding

Drive Smarter 4.12 explicitly interprets display-capability bit `0x04` as display-location support. The physical RAD 700i returns display capability byte `0x07`, so that bit is set on the tested detector. This establishes capability advertisement; it does not yet physically prove a visible `DISPLAY_LOCATION` result.

The current app sends clear-location only when that capability flag is set:

```text
F5 01 AE
```

For `DISPLAY_LOCATION (0xAD)`, the app accepts five logical inputs:

- threat type: one byte / marked-location identifier;
- distance in feet;
- threat level: current app protocol IDs Yellow=0, Orange=1, Red=2;
- heading in degrees, with negative heading normalized by adding 360 at the callsite;
- reporter/database bit: Database=1, User=0.

If `h = (heading_degrees / 2) & 0xFF`, the five 7-bit-safe payload bytes are:

```text
p0 = threat_type & 0x7F
p1 = (((threat_type & 0x80) >> 7) | (distance_feet << 1)) & 0x7F
p2 = (distance_feet >> 6) & 0x7F
p3 = ((distance_feet >> 13) | (h << 3)) & 0x7F
p4 = (((threat_level & 0x03) << 5) | (h >> 4) | ((reporter_id & 0x01) << 4)) & 0x7F
```

The resulting frame is:

```text
F5 06 AD p0 p1 p2 p3 p4
```

The app suppresses the write when threat type is zero or display-location capability is absent. This replaces the previous compatible-family-only packing hypothesis with exact current Drive Smarter construction. Live RAD 700i use remains unvalidated, so normal toolbox hardware writes should stay blocked.

Direction matters for opcode `0xAE`: client-to-detector `0xAE` is `DISPLAY_CLEAR_LOCATION`, while detector-to-client `0xAE` is `RADAR_OPTIONS_INFO_RESPONSE`.

## Turn-by-turn protocol family

Drive Smarter carries a separate Cedar turn-by-turn BLE transport:

- service: `52AFFC3A-6424-11EC-90D6-0242AC120003`;
- TX: `B5E22DFB-31EE-42AB-BE6A-9BE0837AA344`;
- RX: `B5E22DFC-31EE-42AB-BE6A-9BE0837AA344`.

These UUIDs and packet builders are exact current-app static evidence, but this repository has not observed them on the physical RAD 700i. They are therefore application-family evidence, not a claimed RAD 700i capability.

The TBT frame envelope is:

```text
AA 55 <length-le16> <payload> <checksum-le16> BB 66
```

For the simple one-byte requests in this build, the app constructs:

```text
AA 55 01 00 01 01 00 BB 66   capabilities request
AA 55 01 00 02 02 00 BB 66   supported-maneuvers request
AA 55 01 00 04 04 00 BB 66   cancel request
```

The checksum helper used for these request forms sums payload bytes. The maneuver builder sums payload bytes as unsigned values and emits the low 16 bits little-endian.

The current maneuver request type is `3`. Its logical payload consists of 19 fixed bytes followed by a UTF-8 maneuver text string and a NUL terminator. The app sets the 16-bit frame length to `text_utf8_length + 20`.

Fixed maneuver payload fields, in order:

1. request type `3`;
2. maneuver type;
3. reserved zero;
4. detailed maneuver/icon code;
5. reserved zero;
6. exit number;
7. reserved zero;
8. maneuver-modifier-3 value (currently zero);
9. reserved zero;
10-11. distance times 10, low 16 bits, little-endian;
12. distance unit;
13. ETA hours when supported, otherwise zero;
14. ETA minutes when supported, otherwise zero;
15. ETA seconds when supported, otherwise zero;
16-17. lane count, low 16 bits little-endian when supported;
18-19. active-lane count, low 16 bits little-endian when supported;
20+. primary maneuver text in UTF-8 plus NUL.

Distance-unit values:

| Value | Unit |
|---:|---|
| 0 | None |
| 1 | Meters |
| 2 | Kilometers |
| 3 | Feet |
| 4 | Miles |

Maneuver-type values:

| Value | Type |
|---:|---|
| 1 | Turn |
| 2 | New name |
| 3 | Depart |
| 4 | Arrive |
| 5 | Merge |
| 6 | On ramp |
| 7 | Off ramp |
| 8 | Fork |
| 9 | End of road |
| 10 | Continue |
| 11 | Roundabout |
| 12 | Rotary |
| 13 | Roundabout turn |
| 14 | Notification |
| 15 | Exit roundabout |
| 16 | Exit rotary |

Modifier values are `None=0`, `U-turn=1`, `Sharp right=2`, `Right=3`, `Slight right=4`, `Straight=5`, `Slight left=6`, `Left=7`, and `Sharp left=8`.

The app parses TBT response discriminator byte 4. Response type `1` carries capability data: byte 7 enables ETA, byte 8 enables lane data, and byte 9 is the maximum address/text length. Response type `2` marks maneuver support. The app waits for these capability responses before sending maneuver data.

No live turn-by-turn packet should be enabled for the RAD 700i solely from this static evidence.

## Setting value semantics for physically observed IDs

The setting request byte is definitively `ordinal + 1` in the current `RadarSetting.Type` implementation. For several physically queried settings, the current app's parser and resource arrays also give exact value labels. These labels are static application semantics applied to physically observed raw values; they are not equivalent to separately toggling every value on the detector.

| ID | Setting | Current-app value semantics relevant to capture | Physical current |
|---:|---|---|---:|
| `02` | Brightness | 0 Full dark, 1 Minimum, 2 Medium, 3 Maximum, 4 Auto, 5 Last | `01` = Minimum |
| `07` | AutoMute | 0 Off, 1 On, 2 Low, 3 Medium, 4 High | `01` = On |
| `0A` | Voice | two-state current-app enumeration: 0 Off, 1 On | `01` = On |
| `0E` | Units | 0 Imperial, 1 Metric | `00` = Imperial |
| `13` | Cruise alert | numeric 20–160 step 5 plus synthetic Off | `00` = Off |
| `14` | Over speed alert | numeric 20–160 step 5 plus synthetic Off | `00` = Off |
| `15` | Language | 0 English, 1 Spanish, 2 Russian, 3 Chinese | `00` = English |
| `16` | Display color | 0 Amber, 1 Red, 2 Green, 3 Blue, 4 Copper, 5 Orange, 6 Yellow, 7 White | `01` = Red |
| `24` | Detail | 0 Less, 1 More | `01` = More |
| `25` | Screen saver | 0 Off, 1 1 Minute, 2 2 Minutes, 3 3 Minutes | `01` = 1 Minute |
| `26` | Smart power | two-state current-app enumeration: 0 Off, 1 On | `00` = Off |
| `28` | Low voltage alert | two-state current-app enumeration: 0 Off, 1 On | `00` = Off |
| `29` | Quiet drive | two-state current-app enumeration: 0 Off, 1 On | `00` = Off |
| `2B` | K low band enable | two-state current-app enumeration: 0 Off, 1 On | `00` = Off |
| `2C` | Caution area | two-state current-app enumeration: 0 Off, 1 On | `01` = On |

Important exceptions:

- Sensitivity (`01`) uses a current-app resource array whose indices 0–10 are Auto, AutoNoX, City, CityLoX, CityNoX, Highway, AutoLoK, Low, Medium, High, Extreme. The physical RAD 700i reports supported/current value `0x10` (decimal 16), which is outside that array. Therefore `0x10` remains unresolved and must **not** be mislabeled as Extreme (Extreme is decimal 10 / `0x0A`).
- AutoLearn (`10`) has physical `0/1` bytes, but its current handler does not provide a normal value-label array in this build. Preserve the raw value rather than assuming Off/On.
- `0xF4` is the current parser's unsupported-setting sentinel.

## Band-enable bitfield model

Drive Smarter 4.12.0.0 also exposes its band-enable model as byte-index/mask pairs:

| Option | Byte index | Mask |
|---|---:|---:|
| Ku | 0 | `0x40` |
| Laser | 0 | `0x20` |
| SWS | 0 | `0x10` |
| POP | 0 | `0x08` |
| X Band | 0 | `0x01` |
| K Pulse | 1 | `0x10` |
| Shifter Mode | 1 | `0x0C` |
| TSR | 1 | `0x02` |
| RDR | 1 | `0x01` |
| Ka Band Superwide | 0 | `0x04` |
| Ka Band | 1 | `0x60` |
| Ka Narrow 1–7 | 2 | `0x01,02,04,08,10,20,40` |
| Ka Narrow 8–10 | 3 | `0x01,02,04` |
| K Band | 0 | `0x02` |
| K Narrow 1–4 | 3 | `0x08,10,20,40` |
| Strelka | 4 | `0x01` |
| MultaRadar CD | 4 | `0x02` |
| MultaRadar CT | 4 | `0x04` |
| Gatso | 4 | `0x08` |
| Mesta 210c | 5 | `0x01` |
| Mesta Fusion | 5 | `0x02` |
| Dahua | 5 | `0x04` |

The physical RAD 700i capture returned `27 00 00 00 06` for both current and supported band masks. Applying the current app's map to those physically observed bytes yields set fields for X Band, K Band, Ka Band Superwide, Laser, MultaRadar CD, and MultaRadar CT. Byte index 5 is absent in the five-byte RAD 700i response, so Mesta/Dahua fields are unavailable rather than assumed false.

This is a static interpretation of physically observed RAD 700i mask bytes. Multi-bit fields such as Shifter Mode and Ka Band should be preserved as masked numeric values until their value semantics are separately reduced.

## Other parser constraints

The current parser also establishes:

- band-enable current/supported responses are accepted only at total F5 frame lengths 8 or 9 bytes;
- marker-enable current/supported responses are accepted only at total frame length 5 bytes;
- `DISPLAY_CAPABILITIES_RESPONSE (0xA8)`, `GPS_EQUIPPED_RESPONSE (0x81)`, and `SPEED_INFORMATION_REQUEST (0xA6)` carry one payload byte in the accepted form;
- `BLUETOOTH_PROTOCOL_UNLOCK_REQUEST/RESPONSE` use total frame length 13, matching command plus 10-byte challenge/response;
- `BLUETOOTH_SERIAL_NUMBER_RESPONSE (0xA5)` uses total frame length 11 and decodes its payload as UTF-8;
- `STATUS_RESPONSE (0x99)` is accepted at length >=4, but Drive Smarter 4.12 constructs its status object from only the first payload byte;
- model-info type byte `0x03` maps to `COBRA`, which agrees with the captured physical RAD 700i model response beginning with `03`;
- the managed-code/static inspection found no current `DISPLAY_MESSAGE (0x9A)` or `PLAY_TONE (0x9B)` request symbol, consistent with treating those as legacy/family behavior even though Tone 1/2 work physically;
- a broad string scan of the supplied ARM64 split did not reveal an obvious native Cobra/Escort detector-protocol command path; this is a negative search result, not proof that native code can never participate.

The fact that Drive Smarter 4.12 ignores Status bytes after the first weakens the relevance of older compatible-family "Status-embedded A9 alert tail" behavior for this app version. Longer tails should still be preserved as raw data if encountered, but not preferentially decoded as alerts without physical evidence.

## Evidence discipline

- Static application analysis is labeled separately from physical RAD 700i observations.
- Existing physical captures remain the authority for saying a command is actually exercised by RAD 700i firmware.
- No APK or decompiled proprietary source is committed.
