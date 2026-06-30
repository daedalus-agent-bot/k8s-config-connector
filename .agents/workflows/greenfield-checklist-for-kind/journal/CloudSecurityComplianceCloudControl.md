# CloudSecurityComplianceCloudControl Greenfield Migration Journal

### Current Step
Step 2: Direct Controller, E2E fixtures and Fuzzer

### Progress Tracking
| Step Number and Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
|---|---|---|---|---|---|
| Step 1: Direct API Types and Identity | [#9024](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/9024) | [#9040](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/9040) | Merged | 2026-06-03 | 2026-06-03 |
| Step 2: Direct Controller, E2E & Fuzzer | [#9368](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/9368) | [#10991](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10991) | PR Created | 2026-06-05 | |
| Step 3: mockGCP Generation | | | Pending | | |
| Step 4: MockGCP Alignment | | | Pending | | |

### Status Updates
* **2026-06-30**: Monitored PR [#10991](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10991). Found ongoing CI failures on `fuzz-roundtrippers`, `unit-tests`, `validate-generated-files`, and `validations`. Re-assigned the PR back to the author bot (`ada-coder-bot`) via REST API to investigate and resolve these issues.
* **2026-06-30**: Monitored PR [#10991](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10991). Found still-failing checks (`fuzz-roundtrippers`, `validate-generated-files`, and `validations`). Re-assigned the PR back to the author bot (`ada-coder-bot`) via REST API to investigate and resolve these failures.
* **2026-06-30**: `ada-coder-bot` investigated and applied fixes for the compilation and `validate-generated-files` failures (updating framework types, generate.sh, and regenerating static_config.go). Force-pushed the updates to PR [#10991](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10991). Awaiting completion of the pending CI checks.
* **2026-06-30**: Identified failing CI checks on PR [#10991](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10991) (including `tests-gcptracker`, `validate-generated-files`, `fuzz-roundtrippers`, and linters). Assigned the PR back to the author bot (`ada-coder-bot`) to investigate and address the failures.
* **2026-06-30**: `ada-coder-bot` has successfully opened a new Pull Request [#10991](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10991) to implement the direct controller, E2E fixtures, and fuzzer. Currently, CI checks are pending. Monitoring the PR status.
* **2026-06-30**: Monitored the progress of Step 2. The sandbox run was initiated on 2026-06-29. Awaiting `ada-coder-bot` to re-submit or recreate a new PR for the direct controller and E2E fixtures implementation.
* **2026-06-29**: Initialized the Greenfield checklist tracking for `CloudSecurityComplianceCloudControl`. Step 1 was successfully completed and merged on 2026-06-03. Step 2 issue #9368 is currently open, but its associated PR #9373 was closed on 2026-06-29 due to merge conflicts and inactivity. We are prompting the assigned coder bot (`ada-coder-bot`) on issue #9368 to resume and submit a new PR.
