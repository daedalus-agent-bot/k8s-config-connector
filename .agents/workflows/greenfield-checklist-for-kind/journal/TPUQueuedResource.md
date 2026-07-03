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
- **2026-07-03**: Monitored Step 1 progress again. Pull request #11251 remains open, with almost all CI checks (including `unit-tests`, `validate-generated-files`, `test-mockgcp`, `validations`, and `tests-e2e-fixtures-dataflow`) now successfully passed. Only two checks (`tests-e2e-fixtures-compute` and `tests-e2e-fixtures-bigquery`) remain in progress. No failures have been reported on the latest commit `2338cc28af1fe1b53beffc84064e89419b8dd28d`.
- **2026-07-03**: Checked Step 1 progress. Pull request #11251 is still open, and a new commit `2338cc28af1fe1b53beffc84064e89419b8dd28d` was submitted. All completed CI checks (including `unit-tests`, `validate-generated-files`, `test-mockgcp`, and `build-images`) are passing, and remaining checks are actively in progress. No active failures have been reported so far.
- **2026-07-03**: Monitored Step 1 progress. Pull request #11251 remains open. The `unit-tests` check is now passing, but the `validations` check has failed because the generated Go clients are out of date. Assigned the PR back to the author bot `lovelace-coder-bot` to regenerate the Go clients (using `make ready-pr`) and push the updates.
- **2026-07-03**: Checked Step 1 progress. Pull request #11251 remains open. Most CI checks have passed (including `unit-tests` and `test-mockgcp`), but the `validations` check is failing due to out-of-date deepcopy code (`zz_generated.deepcopy.go`). Assigned the PR to the author bot `lovelace-coder-bot` to regenerate and push.
- **2026-07-03**: Checked Step 1 progress. Pull request #11251 is still open, and a new commit `6483d775f4c04ae3d803b99cb61b5888299e166d` was submitted. Many CI checks (such as `validate-generated-files` and `test-mockgcp`) are now passing, while `unit-tests`, `smoketest-with-kind`, `fuzz-roundtrippers`, and `validations` are actively in progress. No active failures have been reported on this commit so far.
- **2026-07-03**: Monitored Step 1 progress. Pull request #11251 remains open. The check `validate-generated-files` is now passing, but `unit-tests` and `validations` are still failing. The PR remains assigned to the author bot `lovelace-coder-bot` for continued investigation and fixes.
- **2026-07-03**: Verified PR #11251 remains open with a failing `unit-tests` CI check. Discovered that no assignee was set on the PR, so assigned the author bot `lovelace-coder-bot` to investigate and resolve the failure.
- **2026-07-03**: Monitored Step 1 progress. Pull request #11251 remains open and continues to experience failing CI checks (`unit-tests`, `validate-generated-files`, and `validations`). It remains assigned to the author bot `lovelace-coder-bot` for active investigation and fixes.
- **2026-07-02**: Checked Step 1 progress again. Pull request #11251 is still open but experiencing failing CI checks (`unit-tests`, `validate-generated-files`, and `validations`). It remains assigned to the author bot `lovelace-coder-bot` for ongoing investigation and fixes.
- **2026-07-02**: Checked Step 1 progress. Discovered that a new pull request #11251 was opened by `lovelace-coder-bot` to implement direct types and identity, but it has some failing CI checks (`unit-tests`, `validate-generated-files`, and `validations`). Assigned the PR to the author bot `lovelace-coder-bot` to trigger automated investigation and fixing of the CI failures.
- **2026-07-02**: Initialized the migration journal for TPUQueuedResource. Found that Step 1 issue #10306 is currently open. The previous pull request #10324 was closed due to conflicts/CI failures, and the issue remains open for a new attempt.
