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

## GPS characteristic reported by the seed implementation

- UUID: `0000fe51-8e22-4541-9d4c-21edae82ed19`
- Reported properties: `read`, `notify`
- Reported handle: `0x000e`
- Endpoint evidence: independent public RAD 700i implementation
- Payload interpretation confidence: `hypothesis`

This UUID/handle is **not** promoted from the 2026-09-11 Drive Smarter HCI capture. A search of the exact Drive Smarter 4.12 managed decompilation, base APK DEX strings, and supplied ARM64 native split found no `FE51` UUID literal. That absence does not disprove the endpoint, but it means the current Drive Smarter build is not additional evidence for it.

## Drive Smarter turn-by-turn service — static application evidence

The exact Drive Smarter 4.12 build declares a separate Cedar turn-by-turn UUID family:

- service: `52affc3a-6424-11ec-90d6-0242ac120003`
- TX: `b5e22dfb-31ee-42ab-be6a-9be0837aa344`
- RX: `b5e22dfc-31ee-42ab-be6a-9be0837aa344`
- Confidence for **application support:** `inferred`
- Confidence for **RAD 700i physical availability:** `unknown`

The app groups all three UUIDs into its turn-by-turn UUID list and contains packet construction/parsing for that transport. These UUIDs have not yet been confirmed in a sanitized physical RAD 700i GATT enumeration, so they are not part of the model's confirmed BLE surface.

## Still-needed GATT work

Highest-value next step is a complete sanitized RAD 700i enumeration that explicitly checks for the turn-by-turn service/TX/RX UUIDs above. Additional useful data includes advertisement fields, descriptors/CCCDs, handles across firmware versions, and whether bonding/pairing behavior changes between Android/iOS/desktop clients.
