# Greenfield Migration Checklist: StorageBatchOperationsJob

## Current Step
Step 1: Direct API Types and Identity and Reference Types Pattern

## Progress Tracking

| Step Number | Step Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Direct API Types and Identity and Reference Types Pattern | [#10300](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10300) | [#11238](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11238) | PR Created (CI Passed) | 2026-06-15 | - |
| 2 | Direct Controller, E2E fixtures and Fuzzer | - | - | Not Started | - | - |
| 3 | mockGCP generation | - | - | Not Started | - | - |
| 4 | MockGCP Alignment with RealGCP | - | - | Not Started | - | - |

## Updates
- **2026-07-03**: Verified that all CI checks on PR #11238 have successfully passed! The PR is now ready for human OWNER review and merge.
- **2026-07-03**: Verified that `hopper-coder-bot` resolved the `unit-tests` failure by updating `alpha-missingfields.txt` and pushed a new commit. All previously failed checks are currently in progress or successful, with no failed checks on the latest commit.
- **2026-07-03**: Checked the status of Step 1 PR #11238. Most CI checks are now passing (including unit-tests-operator and validate-generated-files which were previously failing), but `unit-tests` continues to fail. Assigned the PR back to `hopper-coder-bot` to investigate the unit-tests failure.
- **2026-07-02**: Initialized the migration journal. Found Step 1 PR #11238 is failing several CI checks (unit-tests, unit-tests-operator, validate-generated-files, validations). Assigning the PR back to `hopper-coder-bot` for resolution.
