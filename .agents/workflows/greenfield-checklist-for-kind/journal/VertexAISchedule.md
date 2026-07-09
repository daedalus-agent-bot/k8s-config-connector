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
- **2026-07-07**: Step 1 is in progress. Issue [#9248](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/9248) is open and PR [#11388](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11388) is created but currently has failing checks. Assigned the PR to `ada-coder-bot` to trigger automated retry and fix the checks.
- **2026-07-07**: `ada-coder-bot` pushed a new commit `b98e34c8` addressing the CI failures (including `validate-generated-files`, `unit-tests`, and `validations`) by implementing handwritten mapper overrides in `pkg/controller/direct/aiplatform/vertexaischedule_mapper.go`, adding registry/test exceptions, and regenerating golden files.
- **2026-07-07**: Verified that the check-runs completed with failures on `validate-generated-files` and `validations`. Assigned the PR back to `ada-coder-bot` to trigger automated analysis and address the remaining errors.
- **2026-07-07**: Verified that the check-runs for commit `db1b678d` completed. While the `aiplatform` E2E test suite passed, the `validations` check-run failed due to unregenerated Go clients. Assigned the PR back to `ada-coder-bot` to run `make ready-pr` and fix the checks.
- **2026-07-07**: Verified that the latest commit `ff6d48b5` successfully resolved the failures. All 195+ check-runs are completely green and ready for review/merging by human OWNERS.
- **2026-07-08**: Monitored PR [#11388](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11388). Confirmed that the PR is open but has merge conflicts. Assigned the PR back to `ada-coder-bot` to resolve the conflicts.
- **2026-07-08**: Confirmed that merge conflicts were successfully resolved and commit `9f75b001` was pushed. The new CI check suite completed with a failure on the `tests-e2e-fixtures` run due to unrelated flaky tests `videostitchercdnkey-maximal/minimal`. Assigned the PR back to `ada-coder-bot` to trigger a retry.
- **2026-07-09**: Confirmed commit `0a0b93a2` was pushed to add missing `VideoStitcherCDNKey` mock golden logs to unblock CI. The newly triggered CI checks completed with most passing, except for `tests-e2e-fixtures-apigateway` which failed due to a transient rate-limiting flake. Assigned the PR back to `ada-coder-bot`, but the watch daemon gave up after reaching its retry limit.
- **2026-07-09**: Monitored PR [#11388](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11388). A new set of CI presubmit check-runs was triggered. While they were running, another check completed with a failure on the unrelated `tests-scenarios-powertool` suite. Reassigned the PR back to `ada-coder-bot` via the REST API to trigger another analysis and retry.
- **2026-07-09**: Verified that the latest set of CI check-runs (for head commit `28ab0640`) is currently in progress, with almost all checks pending. We are actively monitoring these runs and waiting for human OWNER review and merge of Step 1 before transitioning to Step 2.
