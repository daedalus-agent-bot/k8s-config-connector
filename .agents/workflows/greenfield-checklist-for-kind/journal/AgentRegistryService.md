# Greenfield Migration Journal: AgentRegistryService

## Current Step
- **Step 1**: Direct API Types and Identity and Reference Types Pattern

## Migration Progress

| Step | Step Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
|---|---|---|---|---|---|---|
| 1 | Direct API Types & Identity | [#11475](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/11475) | [#12015](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12015) | Open (Failing CI, Paused with `overseer/stop`) | 2026-07-29 | - |
| 2 | Direct Controller & E2E Fixtures | - | - | Not Started | - | - |
| 3 | mockGCP Generation | - | - | Not Started | - | - |
| 4 | MockGCP Alignment with RealGCP | - | - | Not Started | - | - |

## Status Update Notes

### 2026-09-10
- Re-evaluated the status of `AgentRegistryService` Greenfield migration.
- Confirmed that Step 1 Pull Request [#12015](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12015) is still open and paused under the `overseer/stop` label.
- Verified that the CI checks (`presubmit-gatekeeper`, `tests-e2e-fixtures`, `validate-generated-files`, `validations`) are still failing.
- Respecting the `overseer/stop` label as mandated by safety guardrails. No new actions or subsequent step issues will be triggered until the block is resolved and the PR is successfully merged.

### 2026-09-09
- Initialized greenfield migration checklist and journal tracking for `AgentRegistryService`.
- Identified that Step 1 GitHub Issue [#11475](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/11475) and Pull Request [#12015](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12015) already exist.
- Step 1 PR [#12015](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12015) is currently open but failing CI checks (`presubmit-gatekeeper`, `tests-e2e-fixtures`, `validate-generated-files`, `validations`).
- The PR was paused by `argus-watcher-bot` with the `overseer/stop` label after 3 unsuccessful attempts to fix CI.
- Under the orchestration guidelines, we must respect the stop label and wait for manual intervention or a new commit to resolve the block before we can proceed to subsequent steps. No new issues for Step 2 will be created until Step 1 is merged successfully.
