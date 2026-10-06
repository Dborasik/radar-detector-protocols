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

The parser treats Status as an object derived from the first payload byte. It expects a one-byte payload for speed-information requests and a one-byte payload for display-capabilities responses. The alert field-level decoding still needs to be reduced into protocol documentation; do not infer the exact RAD 700i alert layout merely from the existence of these parser branches.

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

- observed client `F5 01 AF` corresponds to Drive Smarter symbol `DISABLE_ENABLE_RADAR`; the paired detector `F5 02 AB 00` is named `RADAR_ENABLE_DISABLE_SUPPORT_RESPONSE`. The exact zero-payload AF operation is not replayed by the toolbox because the symbol alone does not prove whether it is a capability query or a state transition.
- observed client `F5 02 D1 00` corresponds to `RADAR_OPTIONS_REQUEST`. Payload semantics and response association still need reduction before replay.

Notably, the current Drive Smarter request enum does **not** contain the older compatible-family arbitrary `DISPLAY_MESSAGE (0x9A)` or `PLAY_TONE (0x9B)` request symbols. The physical RAD 700i still responds audibly to tested `0x9B` selectors, but these operations appear to be legacy/family behavior rather than current Drive Smarter 4.12 request-enum features.

## Alert parser structure

Current Drive Smarter statically confirms two distinct record widths:

- `ALERT_RESPONSE (0x82)`: payload is divided into 4-byte alert records.
- `ALERT_RESPONSE_FRONT_REAR (0xA9)`: payload is divided into 5-byte alert records.

For each record, Drive Smarter constructs the same alert-domain object using a four-argument or five-argument constructor respectively. The parser applies alert-type/strength filtering before retaining an alert. Exact meanings of the constructor fields are the next static-analysis target.

This moves the **record widths** from older compatible-family hypothesis to current Drive Smarter application evidence. It does not yet prove that an active RAD 700i uses the A9 form or establish exact band/frequency/direction/strength field semantics.

## Other parser constraints

The current parser also establishes:

- band-enable current/supported responses are accepted only at total F5 frame lengths 8 or 9 bytes;
- marker-enable current/supported responses are accepted only at total frame length 5 bytes;
- `DISPLAY_CAPABILITIES_RESPONSE (0xA8)`, `GPS_EQUIPPED_RESPONSE (0x81)`, and `SPEED_INFORMATION_REQUEST (0xA6)` carry one payload byte in the accepted form;
- `BLUETOOTH_PROTOCOL_UNLOCK_REQUEST/RESPONSE` use total frame length 13, matching command plus 10-byte challenge/response;
- `BLUETOOTH_SERIAL_NUMBER_RESPONSE (0xA5)` uses total frame length 11 and decodes its payload as UTF-8;
- `STATUS_RESPONSE (0x99)` is accepted at length >=4, but Drive Smarter 4.12 constructs its status object from only the first payload byte;
- model-info type byte `0x03` maps to `COBRA`, which agrees with the captured physical RAD 700i model response beginning with `03`.

The fact that Drive Smarter 4.12 ignores Status bytes after the first weakens the relevance of older compatible-family "Status-embedded A9 alert tail" behavior for this app version. Longer tails should still be preserved as raw data if encountered, but not preferentially decoded as alerts without physical evidence.

## Evidence discipline

- Static application analysis is labeled separately from physical RAD 700i observations.
- Existing physical captures remain the authority for saying a command is actually exercised by RAD 700i firmware.
- No APK or decompiled proprietary source is committed.
