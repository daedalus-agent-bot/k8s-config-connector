# Greenfield Migration Progress: TranslateAdaptiveMtDataset

## Current Step
**Step 2: Direct Controller, E2E fixtures and Fuzzer**

## Progress Tracking Table

| Step | Step Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Direct API Types and Identity | [#10308](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10308) | [#11259](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11259) | Completed | 2026-05-27 | 2026-07-15 |
| 2 | Direct Controller, E2E fixtures and Fuzzer | [#11851](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/11851) | [#11861](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11861) | PR Created | 2026-07-23 | - |
| 3 | mockGCP generation | - | - | Pending | - | - |
| 4 | MockGCP Alignment with RealGCP | - | - | Pending | - | - |

## Status Update Notes
* **2026-08-08**: Checked PR [#11861](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11861) state. Verified that all 195 CI checks are 100% green and successfully passing. The PR is still open, and we continue to wait for a human OWNER to review, approve, and merge it before we can proceed to Step 3.
* **2026-08-08**: Re-monitored Step 2. Checked the status of PR [#11861](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11861) and verified that all 195 CI checks are 100% green and passing. The PR remains open, and we are awaiting a human OWNER to review, approve, and merge it before we can proceed to Step 3.
* **2026-08-08**: Re-monitored Step 2. Re-verified PR [#11861](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11861) after recent rebase and force-push. Confirmed that all CI checks have successfully passed and are 100% green. The PR is ready and we are awaiting a human OWNER to review, approve, and merge Step 2.
* **2026-08-08**: Re-monitored Step 2. Verified that all CI checks for PR [#11861](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11861) have successfully passed and are now 100% green. The PR remains open, and we are currently waiting for a human OWNER to review and merge Step 2 before we can proceed to Step 3.
* **2026-08-08**: Monitored Step 2. Pull Request [#11861](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11861) has failed CI check `unit-tests` due to `pkg/gcpurls` template validation error (`registry_test.go:273: Registered template "//translate.googleapis.com/projects/{project}/locations/{location}/adaptiveMtDatasets/{dataset}" not found in CAI definitions`). Assigned PR back to `hopper-coder-bot` to resolve the test failure.
* **2026-07-23**: Verified Step 1 completed (PR [#11259](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11259) merged). Opened Step 2 issue [#11851](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/11851) for direct controller, E2E fixtures, and fuzzer implementation.
