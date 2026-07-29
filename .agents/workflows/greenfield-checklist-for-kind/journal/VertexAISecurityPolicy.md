# Greenfield Migration Journal: VertexAISecurityPolicy

## Current Step
Step 1: Direct API Types and Identity and Reference Types Pattern

## Progress Tracking Table
| Step | Name | GitHub Issue | Pull Request | Status | Date Started | Date Completed |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Direct API Types and Identity | [#12012](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12012) | [#12041](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12041) | PR Created | 2026-07-29 | |
| 2 | Direct Controller and E2E Fixtures | | | | | |
| 3 | mockGCP Generation | | | | | |
| 4 | MockGCP Alignment | | | | | |

## Status Update Notes
- **2026-07-29**: Verified that all completed CI check-runs for PR #12041 are now passing (including unit-tests, linters, static validations, and e2e fixtures checks). The PR is currently open and awaiting human OWNER approval and merge.
- **2026-07-29**: PR #12041 is open. Inspected the failing `unit-tests` check-run and identified that `TestCRDShortNamePluralization` failed because the plural shortName `gcpvertexaisecuritypolicys` is flagged as an incorrect pluralization of `gcpvertexaisecuritypolicy`. Noticed that `argus-watcher-bot` started investigating the CI failures on the PR, and `neumann-coder-bot` remains assigned to fix it.
- **2026-07-29**: PR #12041 was created by neumann-coder-bot. Checked CI results and found unit tests are failing. Assigned neumann-coder-bot to the PR to investigate and fix the unit-test failures.
- **2026-07-29**: Monitored Step 1 progress. Coder bot is still working on generating direct KRM types and identity for VertexAISecurityPolicy in the sandbox; no PR has been opened yet.
- **2026-07-29**: Step 1 is in progress. Issue [#12012](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12012) is assigned to the coder bot and sandbox work has begun.
- **2026-07-29**: Started migration for VertexAISecurityPolicy. Created Step 1 GitHub issue [#12012](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12012).
