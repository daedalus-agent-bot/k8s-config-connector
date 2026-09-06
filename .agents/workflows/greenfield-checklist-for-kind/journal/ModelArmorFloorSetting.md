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

### 2026-09-06
- Conducted an orchestrator check on PR [#12752](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12752) at 10:22 UTC.
- Verified that all 111 CI check-runs are successfully passing (100% green).
- Checked active reviews and confirmed the automated KCC auto-review has passed. No human reviews have been posted yet.
- The PR remains OPEN and awaiting a human OWNER review and merge to proceed to Step 2.
- Updated the local journal and GitHub progress tracking comment.
- Conducted another check at 12:30 UTC. Verified that all 247 check-runs (including skipped ones) have fully completed with 100% success. The PR is mergeable (no conflicts) and remains open awaiting human OWNER review.
- Conducted another check at 14:46 UTC. Confirmed that all 111+ CI checks on PR [#12752](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12752) remain 100% green and successfully passing. The PR remains OPEN and awaiting a human OWNER review and merge to complete Step 1.
- Updated the local journal and GitHub progress tracking comment.
- Conducted another check at 16:50 UTC. Re-verified all 247 checks (including 111 active/completed runs and skipped tasks) on PR [#12752](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12752) and confirmed they are 100% green and passing. The PR remains OPEN and awaiting human OWNER review and merge to complete Step 1.
- Updated the local journal and GitHub progress tracking comment.
- Conducted another check at 18:57 UTC. Re-verified all checks on PR [#12752](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12752) and confirmed 100% success across all 247 runs (including 111 active/completed tasks). The PR remains OPEN, has zero conflicts, and is waiting for a human OWNER review and merge to complete Step 1.
- Updated the local journal and GitHub progress tracking comment.
- Conducted another check at 21:05 UTC. Verified all checks on PR [#12752](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12752) remain 100% green and successfully passing. The automated KCC auto-review has passed. The PR is labeled with `overseer/ready-for-human` and remains OPEN, awaiting human OWNER review and merge to complete Step 1.
- Updated the local journal and GitHub progress tracking comment.

### 2026-09-05
- Monitored PR [#12752](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12752). Checked all CI check runs and confirmed they remain 100% green with all 111 check-runs successfully passing.
- Checked PR reviews and labels. Confirmed that the KCC Auto-Review has successfully passed and is fully green. The PR is labeled with `overseer/ready-for-human`.
- Currently waiting for a human OWNER review and merge to complete Step 1.
- Updated progress tracking.

### 2026-09-04
- Verified PR [#12752](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12752). Confirmed that all CI checks (including the previously pending `tests-e2e-fixtures-cloudidentity` and `tests-e2e-fixtures-sql-1-of-2`) are fully passing (100% green). The automated KCC review has also passed, and the PR is currently open and awaiting review and merge from the human OWNERS.
- Updated progress tracking.

### 2026-09-03
- Initiated Greenfield Migration tracking for `ModelArmorFloorSetting`.
- Created Step 1 tracking issue [#12748](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12748).
- Identified pre-existing pull request [#11615](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11615) which already implements Step 1 and Step 2. Linked this PR to Step 1.
- Monitored PR [#11615](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11615) and found that it has merge conflicts. Currently waiting for the assignee of child issue [#12748](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12748) (`hopper-coder-bot`) to resolve the conflicts.
- Monitored Step 1 progress. Identified that `hopper-coder-bot` created a new Pull Request [#12752](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12752) to implement Step 1 and resolve the conflicts of the prior PR.
- Linked Step 1 to the new active PR [#12752](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12752).
- Monitored PR [#12752](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12752) CI check-runs. Verified that all completed checks (including `tests-e2e-fixtures-modelarmor`, `smoketest-with-kind`, `test-mockgcp`, `unit-tests`, `validate-manifests`, and `validate-generated-files`) have passed successfully. Currently waiting for the remaining 2 pending checks (`tests-e2e-fixtures-cloudidentity` and `tests-e2e-fixtures-sql-1-of-2`) to finish and the PR to be merged by human owners.
