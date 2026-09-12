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

Compatible-family protocol tables identify `A9` as speed-limit update, `AA` as actual-speed update, and `AB` as overspeed-limit data. This capture directly establishes that the RAD 700i accepts/uses those command IDs in normal Drive Smarter traffic. Exact unit semantics were not independently varied in this capture, so payload interpretation remains conservative.

## Settings discovery traffic

The session also included requests for settings information (`82 <setting-id>`) and matching `8B` / `8A` responses. This establishes that the settings-query family is active on the RAD 700i, but individual setting meanings are not promoted here without one-setting-at-a-time controlled captures.

## Not established by this capture

- `DISPLAY_MESSAGE (9A)` behavior was not exercised.
- `PLAY_TONE (9B)` as a client request was not exercised; `9B` appears as a detector response in the captured settings/query exchange and must not be conflated with the request solely from numeric coincidence.
- Persistent setting changes were not intentionally performed.
- Lockout, marked-location, firmware, flash, power, or reset operations were not tested.
