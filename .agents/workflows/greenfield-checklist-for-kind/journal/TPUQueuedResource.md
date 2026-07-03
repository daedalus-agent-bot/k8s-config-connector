# Greenfield Migration Journal: TPUQueuedResource

## Current Step
Step 1: Direct API Types and Identity and Reference Types Pattern

## Migration Progress

| Step | Step Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
|---|---|---|---|---|---|---|
| 1 | Direct API Types and Identity | [#10306](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10306) | [#11251](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11251) | Open | 2026-07-02 | - |
| 2 | Direct Controller & E2E | - | - | Pending | - | - |
| 3 | MockGCP Generation | - | - | Pending | - | - |
| 4 | MockGCP Alignment | - | - | Pending | - | - |

## Notes / Status Updates
- **2026-07-03**: Monitored Step 1 progress. Pull request #11251 remains open. The check `validate-generated-files` is now passing, but `unit-tests` and `validations` are still failing. The PR remains assigned to the author bot `lovelace-coder-bot` for continued investigation and fixes.
- **2026-07-03**: Verified PR #11251 remains open with a failing `unit-tests` CI check. Discovered that no assignee was set on the PR, so assigned the author bot `lovelace-coder-bot` to investigate and resolve the failure.
- **2026-07-03**: Monitored Step 1 progress. Pull request #11251 remains open and continues to experience failing CI checks (`unit-tests`, `validate-generated-files`, and `validations`). It remains assigned to the author bot `lovelace-coder-bot` for active investigation and fixes.
- **2026-07-02**: Checked Step 1 progress again. Pull request #11251 is still open but experiencing failing CI checks (`unit-tests`, `validate-generated-files`, and `validations`). It remains assigned to the author bot `lovelace-coder-bot` for ongoing investigation and fixes.
- **2026-07-02**: Checked Step 1 progress. Discovered that a new pull request #11251 was opened by `lovelace-coder-bot` to implement direct types and identity, but it has some failing CI checks (`unit-tests`, `validate-generated-files`, and `validations`). Assigned the PR to the author bot `lovelace-coder-bot` to trigger automated investigation and fixing of the CI failures.
- **2026-07-02**: Initialized the migration journal for TPUQueuedResource. Found that Step 1 issue #10306 is currently open. The previous pull request #10324 was closed due to conflicts/CI failures, and the issue remains open for a new attempt.
