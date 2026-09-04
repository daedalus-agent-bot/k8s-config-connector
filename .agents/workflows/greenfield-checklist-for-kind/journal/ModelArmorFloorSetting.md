# Migration Journal: ModelArmorFloorSetting

Current Step: **Step 1: Direct KRM Types & Identity**

## Progress Tracking

| Step | Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
|------|------|--------------|---------------------|--------|--------------|----------------|
| 1    | Direct KRM Types, Identity & Reference | [#12748](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12748) | [#12752](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12752) | PR Created | 2026-09-03 | |
| 2    | Direct Controller, E2E fixtures & Fuzzer | | | | | |
| 3    | MockGCP generation | | | | | |
| 4    | MockGCP Alignment with RealGCP | | | | | |

## Status Update Notes

### 2026-09-04
- Verified PR [#12752](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12752). Confirmed that all CI checks (including the previously pending `tests-e2e-fixtures-cloudidentity` and `tests-e2e-fixtures-sql-1-of-2`) are fully passing (100% green). The PR is currently open and awaiting review and merge from the human OWNERS.
- Updated progress tracking.

### 2026-09-03
- Initiated Greenfield Migration tracking for `ModelArmorFloorSetting`.
- Created Step 1 tracking issue [#12748](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12748).
- Identified pre-existing pull request [#11615](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11615) which already implements Step 1 and Step 2. Linked this PR to Step 1.
- Monitored PR [#11615](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11615) and found that it has merge conflicts. Currently waiting for the assignee of child issue [#12748](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12748) (`hopper-coder-bot`) to resolve the conflicts.
- Monitored Step 1 progress. Identified that `hopper-coder-bot` created a new Pull Request [#12752](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12752) to implement Step 1 and resolve the conflicts of the prior PR.
- Linked Step 1 to the new active PR [#12752](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12752).
- Monitored PR [#12752](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12752) CI check-runs. Verified that all completed checks (including `tests-e2e-fixtures-modelarmor`, `smoketest-with-kind`, `test-mockgcp`, `unit-tests`, `validate-manifests`, and `validate-generated-files`) have passed successfully. Currently waiting for the remaining 2 pending checks (`tests-e2e-fixtures-cloudidentity` and `tests-e2e-fixtures-sql-1-of-2`) to finish and the PR to be merged by human owners.
