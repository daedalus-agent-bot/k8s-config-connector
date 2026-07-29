# VertexAIModel Greenfield Migration Journal

## Current Step
- **Step 1: Direct API Types and Identity and Reference Types Pattern**

## Migration Progress

| Step | Name | Issue | Pull Request | Status | Date Started | Date Completed |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Direct API Types and Identity and Reference Types Pattern | [Issue #12031](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12031) | [PR #12034](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12034) | PR Created | 2026-07-29 | - |
| 2 | Direct Controller, E2E fixtures and Fuzzer | - | - | Pending | - | - |
| 3 | mockGCP generation | - | - | Pending | - | - |
| 4 | MockGCP Alignment with RealGCP | - | - | Pending | - | - |

## Status Update Notes
- **2026-07-29**: Verified that PR #12034 has successfully passed all CI checks. The PR is currently open and awaiting human OWNER review and approval before merging.
- **2026-07-29**: Verified that PR #12034 is open with all completed CI checks successfully passing. 9 fixture-related tests remain in-progress, which are being actively monitored.
- **2026-07-29**: Checked the status of PR #12034. The PR remains open with several failing CI checks (including `unit-tests`, `golangci-lint`, and `validations`). The AI Factory via `argus-watcher-bot` and `lovelace-coder-bot` is actively investigating and working on fixing the failures.
- **2026-07-29**: Monitored PR #12034. Verified that several checks are currently failing (including `unit-tests`, `golangci-lint`, and `validations`). Re-assigned the PR back to the author bot `lovelace-coder-bot` via the REST API to ensure the workflow is triggered for fixing.
- **2026-07-29**: Identified open PR #12034 for Step 1 with failing checks. Assigned the PR to the author bot `lovelace-coder-bot` to investigate and fix the CI failures.
- **2026-07-29**: Started migration of `VertexAIModel`. Created the tracking journal, opened the GitHub issue for Step 1 ([Issue #12031](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12031)), and verified that the coder bot is currently working on generating the types in a sandbox.
