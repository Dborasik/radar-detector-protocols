# Research workflow

A reproducible protocol contribution should follow a simple sequence.

## 1. Record the test environment

Record model, hardware revision if visible, firmware, companion app version, phone/host OS, radio adapter, and capture tooling.

## 2. Enumerate the transport

For BLE, record advertisements, service UUIDs, characteristic UUIDs, properties, descriptors, and observed handles. For other transports, record equivalent endpoints and framing.

## 3. Establish a baseline

Capture an idle session before changing settings or creating an alert.

## 4. Change one variable at a time

Examples:

- X vs K vs Ka vs laser alert
- signal level changes
- mute/unmute
- sensitivity mode
- GPS lock/no lock
- individual setting toggles

Single-variable tests make field attribution substantially more reliable.

## 5. Preserve raw evidence

Keep raw captures when legally and practically possible. Publish sanitized versions with redaction metadata rather than reconstructed packets.

## 6. Reproduce

Repeat the test. When possible, reproduce on a second device or firmware revision before marking a claim `confirmed`.

## 7. Document uncertainty

A useful `hypothesis` is better than a false `confirmed` claim.
