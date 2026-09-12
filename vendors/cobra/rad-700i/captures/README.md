# RAD 700i captures

Capture artifacts in this directory must be sanitized before publication. Do not commit raw system-wide Bluetooth snoop logs, account identifiers, phone identifiers, location history, or unrelated-device traffic.

## Available evidence

- [`2026-09-11-drive-smarter-session.md`](2026-09-11-drive-smarter-session.md) — sanitized summary of an Android Bluetooth HCI snoop capture from a physical RAD 700i connected normally to Drive Smarter. Documents the observed F5 framing, client/detector authentication exchanges, protocol handles, query/response traffic, and recurring speed-related writes.

For raw captures retained privately during analysis, record a cryptographic hash in the sanitized summary so future work can verify it came from the same source without publishing unrelated Bluetooth traffic.
