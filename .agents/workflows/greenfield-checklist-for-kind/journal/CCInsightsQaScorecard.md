# CCInsightsQaScorecard Greenfield Migration Journal

## Current Step
**Step 1**: Direct API Types, Identity and Reference Types Pattern

## Progress Tracking

| Step | Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
|------|------|--------------|---------------------|--------|--------------|----------------|
| 1 | Direct API Types, Identity and Reference Types Pattern | [#11403](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/11403) | [#11420](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11420) | PR Created | 2026-07-07 | - |
| 2 | Direct Controller, E2E fixtures and fuzzer | - | - | - | - | - |
| 3 | mockGCP generation | - | - | - | - | - |
| 4 | MockGCP Alignment with RealGCP | - | - | - | - | - |

## Status Updates / Log
* **2026-07-07**: Monitored PR [#11420](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11420) status. The PR remains open, and the author bot `ada-coder-bot` is still assigned to resolve the failing checks. No new commits have been pushed since the last check.
* **2026-07-07**: Re-verified PR [#11420](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11420) status. The PR is open and currently assigned to `ada-coder-bot`. The bot is actively working in its sandbox to resolve the failing checks (`unit-tests`, `validate-generated-files`, and `validations`).
* **2026-07-07**: Pull Request [#11420](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11420) was created by `ada-coder-bot`. Verified CI checks: `unit-tests` and `validate-generated-files` failed. Assigned the PR back to `ada-coder-bot` to run `dev/tasks/generate-types-and-mappers` and update `alpha-missingfields.txt` to fix these failures.
* **2026-07-07**: Confirmed `ada-coder-bot` is actively working on issue #11403 in an initialized sandbox. Awaiting PR creation.
* **2026-07-07**: Monitored Step 1 progress. Issue #11403 is open and assigned to `ada-coder-bot`. Sandbox environment initialized, awaiting PR creation.
* **2026-07-07**: Restarted Step 1 by creating a new GitHub issue #11403 under the clean Greenfield workflow. The previous attempt (#8666 / PR #8701) was closed due to conflicts and memory exhaustion.
* **2026-07-07**: Initialized migration tracking journal. Checked existing issue #8666 for Step 1. Found that previous PR #8701 was closed due to merge conflicts and CI memory limitations. Step 1 is currently open and needs a new PR.
