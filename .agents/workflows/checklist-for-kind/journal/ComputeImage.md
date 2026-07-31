# Migration Journal: ComputeImage

Current Step: Step 6 - Validate Direct Promotion

## Progress Tracking

| Step | Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Direct API Types | [#9984](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/9984) | [#10072](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10072) | Merged | 2026-06-13 | 2026-06-19 |
| 2 | Identity and Reference Types Pattern | [#10527](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10527) | [#10531](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10531) | Merged | 2026-06-19 | 2026-06-20 |
| 3 | Create a Round-Trip KRM Fuzzer | [#10558](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10558) | [#10561](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10561), [#10578](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10578) | Merged | 2026-06-20 | 2026-06-21 |
| 4 | Ensure MockGCP matches real gcp behavior | [#10564](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10564) | [#10568](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10568) | Merged | 2026-06-20 | 2026-06-20 |
| 5 | Implement Direct Controller & E2E Fixtures | [#11358](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/11358) | [#11359](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11359) | Merged | 2026-06-20 | 2026-07-09 |
| 6 | Validate Direct Promotion | [#12073](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12073) | [#12098](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12098) | PR Created | 2026-07-29 | N/A |

## Notes

- **2026-07-31**: Verified that all CI checks on Pull Request [#12098](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12098) continue to pass. The PR is fully green and awaiting human OWNER review and merge.
- **2026-07-30**: All CI checks on Pull Request [#12098](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12098) have successfully passed. The PR is now fully green and awaiting human OWNER review and merge.
- **2026-07-30**: Pull request [#12098](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12098) is open but has failing `tests-e2e-fixtures-compute` CI checks. Assigning the PR back to the author bot `lovelace-coder-bot` to investigate and resolve the failures.
- **2026-07-30**: Sandbox environment started by `argus-watcher-bot` for `lovelace-coder-bot` to begin working on the validation of direct promotion for `ComputeImage` under issue [#12073](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12073).
- **2026-07-29**: Initialized the migration checklist journal for `ComputeImage`. Steps 1 through 5 have already been successfully completed and merged. Created the issue [#12073](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12073) to initiate Step 6 (Validate Direct Promotion).
