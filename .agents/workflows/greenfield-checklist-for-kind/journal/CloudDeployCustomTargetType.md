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
- **2026-09-11 (Update 5)**: Monitored the status of the migration. The pull request [#12866](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12866) remains open and fully validated. All 120+ CI check-runs and automated sandbox reviews continue to pass cleanly (100% green). We are actively waiting for a human OWNER (e.g., `cheftako`) to review and issue `/approve` before we can merge and transition to Step 3 (MockGCP Generation).
- **2026-09-10 (Update 4)**: Re-validated PR [#12866](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12866). All 120+ checks are fully green and validated, and all automated reviews have completed with 100% success. The PR is ready for merging, still waiting for a human code owner's review and `/approve` before we can transition to Step 3 (MockGCP Generation).
- **2026-09-10 (Update 3)**: Confirmed that the pull request [#12866](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12866) remains in 'OPEN' state with all 120+ CI check-runs passing cleanly (100% green). All automated sandbox reviews and checks are complete and fully approved. We are actively waiting for a human OWNER (e.g., `cheftako`) to review and issue `/approve` before transitioning to Step 3.
- **2026-09-10 (Update 2)**: Re-verified that all 120+ CI checks and robot review runs are 100% green and passing. The PR #12866 remains open and fully mergeable, awaiting a final human review and `/approve` from code owners (e.g., `cheftako`) before we can proceed to Step 3.
- **2026-09-10 (Update)**: The developer bot successfully addressed review feedback by implementing MockGCP handlers for `customTargetTypes` and `AdapterForURL` export support for `CloudDeployCustomTargetType`. Pushed fixes for global CAIS exporter compatibility and a payload `name` field golden log alignment mismatch. All 120+ CI check-runs have now passed successfully and all automated reviews are clean and green. The PR remains open, pending human review and `/approve` from code owners (e.g., `cheftako`).
- **2026-09-10**: Verified that all 120+ CI check-runs for PR [#12866](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12866) have completed and passed 100% successfully. All automated reviews are complete and green. The PR remains open, pending human review and `/approve` from code owners (e.g., `cheftako`). We will continue to monitor the PR and will transition to Step 3 (MockGCP Generation) once it is successfully merged.
- **2026-09-09**: Verified that the pull request [#12866](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12866) has been opened for Step 2. CI checks are currently running.
- **2026-09-09**: Initialized the greenfield migration journal. Checked prior step status: Step 1 (API types, identity, reference, fuzzer) was completed and merged in PRs #5245 and #6905. Created GitHub issue #12851 for Step 2 (Implement direct controller, E2E fixtures, and fuzzer) and marked it as `Open`.
