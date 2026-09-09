# Packet notes

This file expands on `protocol.yaml`. It deliberately labels uncertain decoding rather than converting implementation assumptions into protocol facts.

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

All nonzero values are powers of two. That pattern alone is **not** enough to establish that the byte is a bitfield. A multi-signal capture is needed.

### Byte 1

The seed implementation treats byte 1 as signal strength and caps the application-visible result at `10`. That proves neither that the wire value is limited to 0–10 nor that it is linear. Controlled attenuation or repeated real-world captures are needed.

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

The fallback is especially tentative and should not be implemented as a normative format without captures.

## Needed captures

Highest-value captures:

1. Idle/no alert.
2. X, K, Ka, and laser independently.
3. Multiple signal strengths of one fixed-frequency source.
4. Two simultaneous alert sources if the detector exposes both.
5. GPS characteristic with no fix, first fix, stationary fix, and moving fix.
6. Every detector setting changed one at a time while BLE traffic is captured.
