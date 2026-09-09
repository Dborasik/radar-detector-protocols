# Security and sensitive-data reporting

This repository primarily contains protocol documentation, schemas, validation tooling, and sanitized research artifacts. The main security risks are accidental publication of secrets/private data, malicious contribution content, and vulnerabilities in repository tooling or CI.

## Do not publish sensitive data in a public issue or PR

Do not include:

- credentials, API keys, tokens, or cookies;
- personal GPS/location history;
- persistent Bluetooth/Wi-Fi device addresses when they identify a real device;
- serial numbers or account identifiers;
- private captures containing unrelated user/device traffic;
- private local paths, usernames, or hostnames when they identify a contributor or system;
- confidential vendor material you are not authorized to disclose.

If you discover sensitive information already committed to the repository, do not quote or duplicate it in a new public issue.

## Reporting

Use GitHub's private vulnerability reporting feature for this repository when it is available. Include only the information needed to reproduce and remediate the problem.

If private vulnerability reporting is unavailable, open a public issue containing only a non-sensitive description that asks a maintainer to establish a private reporting channel. Do not include the sensitive material itself.

## Supported repository state

Security fixes are applied to the current active branches. Historical protocol observations are research records and may intentionally describe obsolete firmware behavior; that does not imply old firmware is supported or recommended.
