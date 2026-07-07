# Greenfield Migration Journal: VertexAISchedule

## Current Step
Step 1: Direct API Types and Identity and Reference Types Pattern

## Progress Tracking

| Step | Step Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
|------|-----------|--------------|---------------------|--------|--------------|----------------|
| 1 | Direct API Types & Identity | [#9248](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/9248) | [#11388](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11388) | PR Created | 2026-07-06 | |
| 2 | Direct Controller & E2E | | | Planned | | |
| 3 | mockGCP generation | | | Planned | | |
| 4 | MockGCP Alignment | | | Planned | | |

## Status Updates
- **2026-07-07**: Initialized Greenfield migration checklist for `VertexAISchedule`.
- **2026-07-07**: Step 1 is in progress. Issue [#9248](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/9248) is open and PR [#11388](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11388) is created but currently has failing checks. Assigning the PR to `ada-coder-bot` to trigger automated retry and fix the checks.
- **2026-07-07**: Verified that PR [#11388](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11388) is still open with failing CI checks. The `argus-watcher-bot` has successfully acknowledged the failures and initiated an investigation. The PR remains assigned to `ada-coder-bot`, and we are monitoring its progress.
- **2026-07-07**: `ada-coder-bot` pushed a new commit `b98e34c8` addressing the CI failures (including `validate-generated-files`, `unit-tests`, and `validations`) by implementing handwritten mapper overrides in `pkg/controller/direct/aiplatform/vertexaischedule_mapper.go`, adding registry/test exceptions, and regenerating golden files. The CI check-runs are currently in progress.
- **2026-07-07**: Verified that the check-runs for commit `b98e34c8` completed with failures on `validate-generated-files` and `validations`. Assigned the PR back to `ada-coder-bot` to trigger automated analysis and address the remaining errors.
- **2026-07-07**: Verified that the check-runs for commit `db1b678d77308cb8cf29dabd57cba33774d84e5a` completed. While the `aiplatform` E2E test suite passed, the `validations` check-run failed due to unregenerated Go clients (`ERROR: Resource Go Clients must be regenerated`). Assigned the PR back to `ada-coder-bot` to run `make ready-pr` and fix the checks.
