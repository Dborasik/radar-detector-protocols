# Repository protection settings

This file documents the GitHub repository settings required to make the contribution policy enforceable rather than advisory.

## Contribution target

- Default development branch: `develop`
- Public contributor pull requests should target: `develop`
- `main` should be treated as a protected release/stable branch when present.

## Required protection for `develop`

Configure a branch ruleset or branch protection rule with all of the following:

- Require a pull request before merging.
- Require at least 1 approving review.
- Require review from Code Owners.
- Dismiss stale pull request approvals when new commits are pushed.
- Require approval of the most recent reviewable push when that option is available.
- Require conversation resolution before merging.
- Require status checks to pass before merging.
- Require the protocol-validation check from `Validate protocol contracts`.
- Require the `owner-approval` check from `Require owner approval`.
- Block force pushes.
- Block branch deletion.

Do not add broad bypass actors for contributor merges. Repository administrators may retain emergency access, but normal changes should go through pull requests.

## Required protection for `main`

When `main` exists, apply at least the same protections as `develop`. Prefer changes to reach `main` only through a PR from an already-reviewed branch.

## Why both CODEOWNERS and CI exist

`.github/CODEOWNERS` causes GitHub to request `@Dborasik` on changes. The `Require owner approval` workflow additionally verifies that a contributor PR has an `APPROVED` review by `@Dborasik` for the **current head commit**.

A contributor push changes the head SHA, causing the owner-approval check to fail until the new head is reviewed and approved.

The workflow intentionally exempts PRs authored by `@Dborasik` because GitHub does not permit PR authors to approve their own pull requests.

## Merge method

Squash merging is preferred for public contributions so each accepted PR produces a concise repository history entry. Merge or rebase may still be used when preserving commit structure is materially useful.
