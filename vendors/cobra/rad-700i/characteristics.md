# BLE characteristics

The UUIDs below are the currently known BLE entry points. Numeric GATT handles are observations only and may change with firmware/GATT-table revisions; clients should discover by UUID.

## Cobra primary service

- UUID: `2a668fa4-2902-4468-8568-3ebe69a930a0`
- Confidence: `observed`
- Evidence: physical RAD 700i GATT inventory associated with the 2026-09-11 Drive Smarter capture

## Client -> detector protocol characteristic

- UUID: `b5e22dea-31ee-42ab-be6a-9be0837aa344`
- Reported property on the tested unit: `write`
- ATT value handle in the Android HCI capture: `0x0022`
- Firmware/version response observed in the same session: `M1.2.3.6`
- Confidence: `observed`

Drive Smarter transmitted F5-framed authentication, status/query, settings-sync, and speed-related packets on this characteristic.

## Detector -> client / alert characteristic

- UUID: `b5e22deb-31ee-42ab-be6a-9be0837aa344`
- Reported properties: `read`, `notify`
- Observed ATT value handle: `0x0024`
- Confidence: `observed`

The 2026-09-11 capture confirms that this characteristic carries framed protocol responses/challenges in addition to the alert stream documented by the initial public implementation.

## GPS characteristic

- UUID: `0000fe51-8e22-4541-9d4c-21edae82ed19`
- Reported properties: `read`, `notify`
- Observed handle: `0x000e`
- Characteristic existence/properties confidence: `observed`
- Payload interpretation confidence: `hypothesis`

## Still-needed GATT work

Useful future contributions include a complete sanitized enumeration containing advertisement data, descriptors/CCCDs, handles across firmware versions, and whether bonding/pairing behavior changes between Android/iOS/desktop clients.
