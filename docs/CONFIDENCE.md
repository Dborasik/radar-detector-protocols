# Confidence model

Confidence describes how strongly the repository currently supports a protocol claim.

| Level | Meaning | Typical evidence |
|---|---|---|
| `confirmed` | Reproduced independently or documented authoritatively. | Vendor docs, multiple independent captures/tests. |
| `observed` | Seen working on real hardware, but not yet independently reproduced by this project. | Physical-device capture or tested third-party implementation. |
| `inferred` | Evidence is real, but the field's meaning or encoding is not completely isolated. | Correlated byte changes, implementation assumptions that fit tests. |
| `hypothesis` | Plausible explanation awaiting a controlled test. | Pattern analysis, tentative parser. |
| `disputed` | Credible sources conflict. | Different firmware/revisions or contradictory reproductions. |
| `unknown` | No claim is currently made. | Reserved/undecoded bytes. |

## Promotion rules

A claim should generally move:

`hypothesis -> inferred -> observed -> confirmed`

Promotion should be evidence-driven. A popular implementation is not automatically `confirmed`.

## Firmware scope

A claim can be `confirmed` for one firmware version and `unknown` for another. Store scope instead of silently generalizing.
