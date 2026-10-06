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

The same build contains a typed `RadarRequest` enum with symbolic requests for settings information/change/request, band enables, version/model/status/GPS/display queries, display location/clear, mute, authentication, speed limit/current speed/overspeed data, radar enable/disable, radar options, and turn-by-turn operations.

Only request values independently extracted or physically observed should be promoted into the RAD 700i contract. The enum's complete numeric request map is the next static-analysis target.

## Evidence discipline

- Static application analysis is labeled separately from physical RAD 700i observations.
- Existing physical captures remain the authority for saying a command is actually exercised by RAD 700i firmware.
- No APK or decompiled proprietary source is committed.
