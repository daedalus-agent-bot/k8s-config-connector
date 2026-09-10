# Greenfield Migration Journal: CloudDeployCustomTargetType

This journal tracks the progress of the Greenfield migration for `CloudDeployCustomTargetType` to a production-ready direct controller.

## Current Status
- **Current Step**: Step 2 (Implement direct controller, E2E fixtures, and fuzzer)

## Progress Tracking

| Step | Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
|------|------|--------------|---------------------|--------|--------------|----------------|
| 1    | Direct API Types & Identity | N/A | [#5245](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/5245), [#6905](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/6905) | `Completed` | 2026-03-04 | 2026-03-11 |
| 2    | Direct Controller, E2E & Fuzzer | [#12851](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12851) | [#12866](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12866) | `PR Created` | 2026-09-09 | |
| 3    | MockGCP Generation | N/A | N/A | `Pending` | | |
| 4    | MockGCP Alignment with RealGCP | N/A | N/A | `Pending` | | |

## Status Update Notes
- **2026-09-10**: Re-checked PR [#12866](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12866) status. The previously failed transient CI flake in `tests-e2e-fixtures-netapp` has been successfully re-run and passed. All currently completed checks are green, with a few remaining checks in a pending state. The PR remains open, awaiting final CI completion and human owner review/approval before merge. We will continue monitoring the PR before starting Step 3.
- **2026-09-09**: Verified that the pull request [#12866](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12866) has been opened for Step 2. CI checks are currently running.
- **2026-09-09**: Initialized the greenfield migration journal. Checked prior step status: Step 1 (API types, identity, reference, fuzzer) was completed and merged in PRs #5245 and #6905. Created GitHub issue #12851 for Step 2 (Implement direct controller, E2E fixtures, and fuzzer) and marked it as `Open`.
