# Drive Smarter BLE session capture — 2026-09-11

This is a sanitized evidence summary derived from an Android Bluetooth HCI snoop capture of a physical Cobra RAD 700i connecting normally to Drive Smarter.

The raw HCI log is intentionally not committed because system-wide Bluetooth snoop logs can contain unrelated-device traffic. Analysis was restricted to the RAD 700i ATT connection and exported to a filtered CSV before deriving this summary.

## Provenance

- Capture date: 2026-09-11
- Capture source: Android Bluetooth HCI snoop log while Drive Smarter connected to a physical RAD 700i
- Filtered CSV SHA-256: `4e71360f0c9fdcbf9f6207b91564c8408bbf39ee445294e72a3ea7285fa8c808`
- RAD 700i ATT connection handle in this capture: `0x040`
- Client -> detector characteristic value handle: `0x0022`
- Detector -> client characteristic value handle: `0x0024`
- Observed protocol framing: `F5 <command-plus-payload-length> <command> [payload]`
- Version query response included ASCII `M1.2.3.6` after byte `0x40`.

Numeric ATT handles are observations only and must not be treated as stable identifiers.

## Initial client authentication

Observed sequence on the TX/RX characteristics:

```text
client -> detector  F5 0B A3 02 07 47 7D 10 05 62 0F 23 00
detector -> client  F5 0B A2 0E 19 26 70 3C 34 42 53 0A 01
client -> detector  F5 02 A5 00
client -> detector  F5 01 94
detector -> client  F5 02 99 03
```

A later reconnect produced the same command ordering with different challenge bytes.

The `A3 -> A2` challenge/response pair is consistent with the compatible-family BLE smartphone-key XTEA transform described by `qoq/esclib.github.io`. This capture therefore establishes use of that F5 authentication exchange on this RAD 700i, while the cryptographic interpretation is additionally corroborated by the public compatible-family implementation.

## Detector-originated challenge

Later in the same established session the detector challenged the client:

```text
detector -> client  F5 0B A1 43 06 50 3F 33 66 67 14 38 00
client -> detector  F5 0B A4 47 22 50 20 2B 11 7E 23 76 00
detector -> client  F5 02 A3 00
detector -> client  F5 02 A6 03
```

The `A1 -> A4` pair exactly matches the compatible-family BLE smartcord-key transform for the captured challenge.

Subsequent inspection of the exact Drive Smarter 4.12 build resolves the following physical `A6 03` frame: the app masks the A6 payload with `0x03`, defines bit 0 as the posted-speed-limit request flag and bit 1 as the actual-speed request flag, so captured value `03` requests both.

## Observed query/response pairs

```text
94 -> 99 03                              status
91 -> 95 03 52 41 44 20 37 30 30 69 00 model info: "RAD 700i"
97 -> 81 01                              GPS-equipped response
89 -> 92 40 4D 31 2E 32 2E 33 2E 36 00 version payload containing "M1.2.3.6"
AC -> A8 07                              display-capabilities response
99 -> 85 0A                              display-length response
```

The command names above are corroborated by the public compatible-family request/response tables; the exact bytes and directions are directly observed on the RAD 700i.

## Observed recurring client updates

Drive Smarter repeatedly transmitted:

```text
F5 03 A9 19 00
F5 03 AA 00 00
F5 02 AB 00
```

Current Drive Smarter static analysis identifies `A9` as posted speed-limit update, `AA` as actual-speed update, and `AB` as overspeed-limit data. This capture directly establishes that the RAD 700i uses those command IDs in normal Drive Smarter traffic. For AB specifically, Drive Smarter emits `00` when its overspeed preference resolves to OFF (`-1`); otherwise it converts a positive configured over-limit value for the active unit mode when needed, adds 64, and sends one byte. The repeated physical `AB 00` therefore matches the exact current-app OFF path.

## Settings discovery traffic

The session also included requests for settings information (`82 <setting-id>`) and matching `8B` / `8A` responses. This establishes that the settings-query family is active on the RAD 700i, but individual setting meanings are not promoted here without one-setting-at-a-time controlled captures.

## Not established by this capture

- `DISPLAY_MESSAGE (9A)` behavior was not exercised.
- `PLAY_TONE (9B)` as a client request was not exercised; `9B` appears as a detector response in the captured settings/query exchange and must not be conflated with the request solely from numeric coincidence.
- Persistent setting changes were not intentionally performed.
- Lockout, marked-location, firmware, flash, power, or reset operations were not tested.


## Sanitized command-inventory reanalysis — 2026-09-29

The original HCI capture was re-parsed offline using only the RAD 700i ATT connection and the observed TX/RX characteristic handles. The raw system-wide snoop remains private. The following exact protocol bytes contain no phone account, Bluetooth address, location history, or unrelated-device payloads.

### Additional read/query traffic directly observed

```text
client -> detector  F5 02 84 00
client -> detector  F5 01 8C
detector -> client  F5 06 8F 27 00 00 00 06
client -> detector  F5 01 86
detector -> client  F5 06 8C 27 00 00 00 06
client -> detector  F5 01 95
detector -> client  F5 03 9B 0B 00
client -> detector  F5 01 92
detector -> client  F5 03 97 1B 00
```

Compatible-family tables name these as settings request, band-enables supported/current requests and responses, and marker-enables supported/current requests and responses. The byte exchanges above are directly observed on the RAD 700i; the semantic names are corroborated by compatible-family research.

The capture also contains:

```text
client -> detector  F5 01 AF
detector -> client  F5 02 AB 00

client -> detector  F5 02 D1 00
```

Subsequent static analysis of the exact Drive Smarter 4.12.0.0 build resolves the first packet as the app's zero-payload radar enable/disable **support query**, paired with `RADAR_ENABLE_DISABLE_SUPPORT_RESPONSE (0xAB)`. It resolves `D1 00` as `getRadarOptions(RadarOption.ALL)`; the physical payload establishes `ALL = 0x00` for this build. No deterministic `AC` response was isolated from the sanitized baseline capture, so response contents remain raw.

### Exact read-only setting discovery observed

Drive Smarter queried these setting IDs with `F5 02 82 <id>`. For each listed ID, the detector returned an `8B` information payload and an `8A` current-value pair:

| ID | 8B information payload after command | 8A current value |
|---:|---|---:|
| `01` | `01 00 07 08 09 10` | `10` |
| `02` | `02 00 01 02 03` | `01` |
| `07` | `07 00 01` | `01` |
| `0A` | `0A 00 01` | `01` |
| `0E` | `0E 00 01` | `00` |
| `10` | `10 00 01` | `01` |
| `13` | `13 14 A0 05` | `00` |
| `14` | `14 14 A0 05` | `00` |
| `15` | `15 00 01` | `00` |
| `16` | `16 07 02 03 01 06` | `01` |
| `24` | `24 00 01` | `01` |
| `25` | `25 00 01 03` | `01` |
| `26` | `26 00 01` | `00` |
| `28` | `28 00 01` | `00` |
| `29` | `29 00 01` | `00` |
| `2B` | `2B 00 01` | `00` |
| `2C` | `2C 00 01` | `01` |

The table above is direct RAD 700i wire evidence. Later Drive Smarter 4.12 static analysis resolves the current-app symbolic names for these observed IDs: `01 Sensitivity`, `02 Brightness`, `07 AutoMute`, `0A Voice`, `0E Units`, `10 AutoLearn`, `13 Cruise alert`, `14 Over speed alert`, `15 Language`, `16 Display color`, `24 Detail`, `25 Screen saver`, `26 Smart power`, `28 Low voltage alert`, `29 Quiet drive`, `2B K low band enable`, and `2C Caution area`.

The same exact app build also resolves most values without changing the detector:

| ID | Current app labels for captured values | Captured current value |
|---:|---|---|
| `01` | `00 Auto`, `07 Low`, `08 Medium`, `09 High`; `10` has no current-app label | `10` = intentionally unmapped |
| `02` | Full dark / Minimum / Medium / Maximum | Minimum |
| `07` | Off / On | On |
| `0A` | Off / On | On |
| `0E` | Imperial / Metric | Imperial |
| `10` | Off / On | On |
| `13` | Off plus 20–160 step 5 | Off |
| `14` | Off plus 20–160 step 5 | Off |
| `15` | English / Spanish | English |
| `16` | White / Green / Blue / Red / Yellow for the captured supported-value order | Red |
| `24` | Less / More | More |
| `25` | Off / 1 Minute / 3 Minute for the captured supported-value order | 1 Minute |
| `26`, `28`, `29`, `2B` | Off / On | Off |
| `2C` | Off / On | On |

These labels are current-app static interpretation applied to physically observed bytes, not a claim that each menu choice was independently toggled on the detector. The Sensitivity `0x10` anomaly is preserved raw because Drive Smarter's own indexed sensitivity resource table has no entry 16.

### Other recurring traffic recovered from the same capture

```text
detector -> client  F5 01 82
detector -> client  F5 01 A7
detector -> client  F5 02 A6 03
client -> detector  F5 02 AB 00
```

Zero-payload `0x82` occurred repeatedly while there was no active radar alert. `A7` was zero-payload on the physical RAD 700i. The exact current-app logic resolves `A6 03` as bit 0 + bit 1, requesting both posted speed-limit and actual-speed data. Client `AB 00` was repeatedly sent by Drive Smarter and current-app code resolves it as the OFF/no-threshold overspeed path.
