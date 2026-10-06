# Physical toolbox observations — 2026-09-29

This is a sanitized evidence summary from an authenticated Radar Detector Toolbox session with a physical Cobra RAD 700i.

No raw system-wide Bluetooth log is published with this observation. No Bluetooth address, phone identifier, account information, GPS coordinates, or unrelated-device traffic is included.

## Transient-control observations

### Tone request

The toolbox sent the one-byte selector form of client request `0x9B`:

```text
F5 02 9B 00
F5 02 9B 01
F5 02 9B 02
```

Observed physical behavior:

- selector `0x00`: no audible effect
- selector `0x01`: audible tone
- selector `0x02`: audible tone

The experiment does not establish semantic names such as "short" or "long"; only the observable outcomes above are promoted.

### Display message

The toolbox sent the compatible-family display-message form `0x9A` with selector `0x09` followed by printable ASCII. No visible display change was observed.

This is recorded as a negative result. It does not prove that the RAD 700i lacks a display-message mechanism.

### Posted speed limit

A client `0xA9` posted-speed-limit update visibly changed the detector's posted speed-limit field. This independently confirms the command interpretation previously inferred from Drive Smarter traffic.

### Current speed

A client `0xAA` current-speed update produced no visible override of the detector's current-speed display during this stationary test. The RAD 700i has built-in GPS, so source precedence remains unresolved.

## Recurring detector traffic

While connected and authenticated, the RX stream repeatedly included frames such as:

```text
F5 01 82
F5 01 A7
F5 02 99 0B
```

Observations:

- `F5 01 82` occurred while no radar alert was active. Compatible-family tables call detector response `0x82` an Alert Response; zero payload is therefore treated as "no active alerts" for the tested RAD 700i.
- `F5 01 A7` was emitted without a payload. Compatible-family implementations associate detector response `0xA7` with an overspeed-warning/data request, but the exact RAD 700i timing/trigger semantics remain to be characterized.
- Status response `0x99` was observed with payload value `0x0B`. Earlier Drive Smarter capture traffic contained `0x03`, so the status byte is state-dependent and must not be treated as a single fixed success constant.

## Safety scope

No setting changes, band changes, firmware/update commands, flash operations, lockout-database operations, marked-location writes, detector power commands, or reset operations were performed for this evidence.
