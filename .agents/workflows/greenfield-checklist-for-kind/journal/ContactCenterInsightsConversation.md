# ContactCenterInsightsConversation Greenfield Migration Journal

**Current Step**: Step 2: Direct Controller, E2E fixtures and Fuzzer

## Migration Progress

| Step | Name | Issue | Pull Request | Status | Date Started | Date Completed |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Direct API Types and Identity and Reference Types Pattern | [#9016](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/9016) | [#9026](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/9026) | Merged | 2026-06-05 | 2026-06-24 |
| 2 | Direct Controller, E2E fixtures and Fuzzer | [#11414](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/11414) | [#11431](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11431) | PR Created | 2026-07-07 | - |
| 3 | mockGCP generation | - | - | Pending | - | - |
| 4 | MockGCP Alignment with RealGCP | - | - | Pending | - | - |

## Notes & Status Updates

* **2026-07-07**: Checked PR #11431 (implementing Step 2) again. Verified that it is OPEN but still has active CI failures. The PR remains assigned to `ada-coder-bot` for investigation and fixes.
* **2026-07-07**: Checked PR #11431 (implementing Step 2). Found that the PR is OPEN but has CI failures (fuzz-roundtrippers, unit-tests, validate-generated-files, validations). Assigned PR #11431 to `ada-coder-bot` to investigate and fix the failures.
* **2026-07-07**: Periodic check: Verified that the direct controller is still being implemented in the sandbox by `ada-coder-bot`. No pull request has been created yet. Step 2 remains in Open status.
* **2026-07-07**: Confirmed that `argus-watcher-bot` has acknowledged Step 2 (Issue #11414) and started implementing the direct controller in a sandbox. Awaiting pull request creation.
* **2026-07-07**: Step 1 is confirmed fully complete and merged as of 2026-06-24 (commit fa3f7333f9). Created Issue #11414 to track Step 2 (Direct Controller, E2E fixtures and Fuzzer). Closed the completed Step 1 issue #9016.
