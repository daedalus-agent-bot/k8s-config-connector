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
- **2026-09-10 (Update)**: The developer bot successfully addressed review feedback by implementing MockGCP handlers for `customTargetTypes` and `AdapterForURL` export support for `CloudDeployCustomTargetType`. Pushed fixes for global CAIS exporter compatibility and a payload `name` field golden log alignment mismatch. All 120+ CI check-runs have now passed successfully and all automated reviews are clean and green. The PR remains open, pending human review and `/approve` from code owners (e.g., `cheftako`).
- **2026-09-10**: Verified that all 120+ CI check-runs for PR [#12866](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12866) have completed and passed 100% successfully. All automated reviews are complete and green. The PR remains open, pending human review and `/approve` from code owners (e.g., `cheftako`). We will continue to monitor the PR and will transition to Step 3 (MockGCP Generation) once it is successfully merged.
- **2026-09-09**: Verified that the pull request [#12866](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12866) has been opened for Step 2. CI checks are currently running.
- **2026-09-09**: Initialized the greenfield migration journal. Checked prior step status: Step 1 (API types, identity, reference, fuzzer) was completed and merged in PRs #5245 and #6905. Created GitHub issue #12851 for Step 2 (Implement direct controller, E2E fixtures, and fuzzer) and marked it as `Open`.
