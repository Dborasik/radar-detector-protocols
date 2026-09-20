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

### Not confirmed by this capture

`DISPLAY_MESSAGE (0x9A)` and client `PLAY_TONE (0x9B)` were not intentionally exercised. A display-capabilities value of `0x07` is compatible with those features, but capability bits alone are not enough to promote their request packet formats to RAD 700i-observed status.

No firmware/reset/flash/power/lockout/marked-location operation was intentionally tested.

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
