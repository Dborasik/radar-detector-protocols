# BLE characteristics

The UUIDs below are the currently known BLE entry points. Service UUIDs and the complete GATT tree still need to be captured.

## Alert characteristic

- UUID: `b5e22deb-31ee-42ab-be6a-9be0837aa344`
- Reported properties: read, notify
- Observed handle: `0x0024`
- Handle firmware scope: unknown
- Confidence: `observed`

The handle is recorded only to help researchers compare GATT tables. Clients should discover by UUID rather than assuming the numeric handle is stable.

## GPS characteristic

- UUID: `0000fe51-8e22-4541-9d4c-21edae82ed19`
- Reported properties: read, notify
- Observed handle: `0x000e`
- Handle firmware scope: unknown
- Characteristic existence/properties confidence: `observed`
- Payload interpretation confidence: `hypothesis`

## Missing GATT work

A useful next contribution would include a complete sanitized GATT enumeration containing:

- advertisement data
- advertised local name
- service UUIDs
- characteristic UUIDs
- properties
- descriptors/CCCDs
- handles
- firmware version
- whether bonding/pairing was required
