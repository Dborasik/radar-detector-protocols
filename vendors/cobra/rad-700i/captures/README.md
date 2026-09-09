# RAD 700i captures

No raw captures are included in the initial scaffold.

When adding one, include a sidecar YAML file with at least:

```yaml
capture_id: 2026-09-07-example
file: 2026-09-07-example.pcapng
captured_at: "2026-09-07T00:00:00Z"
device:
  model: RAD 700i
  hardware_revision: unknown
  firmware: unknown
host:
  platform: Linux
  adapter: unknown
transport: bluetooth-le
tool: btmon
scenario: Describe exactly what was changed or triggered.
redactions:
  - BLE device address
sha256_original: null
sha256_published: null
notes: []
```

Do not publish precise GPS coordinates, persistent identifiers, account data, or secrets unless they are essential to the protocol claim and safe to disclose.
