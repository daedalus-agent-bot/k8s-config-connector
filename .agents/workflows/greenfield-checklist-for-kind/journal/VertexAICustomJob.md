# Greenfield Migration Journal: VertexAICustomJob

Current Step: Step 1: Direct API Types and Identity and Reference Types Pattern

## Migration Progress

| Step | Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
|------|------|--------------|---------------------|--------|--------------|----------------|
| 1 | Direct API Types and Identity | [Issue #11715](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/11715) | [PR #11724](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11724) | Open | 2026-07-18 | - |
| 2 | Direct Controller & E2E | - | - | Pending | - | - |
| 3 | mockGCP Generation | - | - | Pending | - | - |
| 4 | mockGCP RealGCP Alignment | - | - | Pending | - | - |

## Status Updates
- **2026-07-19**: Re-verified that all CI checks continue to pass successfully. The PR remains open and is awaiting human OWNER review and approval to merge.
- **2026-07-19**: All CI check-runs for PR #11724 have successfully passed. The PR is fully validated and awaiting human OWNER review and approval to merge.
- **2026-07-19**: The `unit-tests` check-run failed again for the updated commit on PR #11724. Specifically, `TestMissingRefs` failed due to unresolved reference warnings for fields `.spec.jobSpec.experiment`, `.spec.jobSpec.experimentRun`, `.spec.jobSpec.models`, `.spec.jobSpec.network`, `.spec.jobSpec.serviceAccount`, and `.spec.jobSpec.tensorboard`. Ensured the PR remains assigned to `ada-coder-bot` to resolve these remaining api-check failures.
- **2026-07-19**: Found open PR #11724. The `unit-tests` check-run failed because of API validation checks (acronyms, missing fields, recursive types, and missing refs). Assigned the PR back to `ada-coder-bot` to resolve these issues.
- **2026-07-18**: Checked the status of Step 1 (#11715). The coder bot has started work in a sandbox, but no Pull Request has been opened yet. Monitoring continues.
- **2026-07-18**: Initialized the greenfield migration for VertexAICustomJob. Created the Step 1 issue (#11715) to generate types and identity.
