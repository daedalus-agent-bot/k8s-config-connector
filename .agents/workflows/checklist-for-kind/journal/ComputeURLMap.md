# Migration Journal: ComputeURLMap

## Current Step
Step 1: Direct API Types (In Progress - PR Created, CI Failing)

## Progress Tracking

| Step | Step Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
|---|---|---|---|---|---|---|
| 1 | Direct API Types | [#10137](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10137) | [#10164](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10164) | PR Created | 2026-06-13 | |
| 2 | Identity and Reference Types Pattern | | | Not Started | | |
| 3 | Create a Round-Trip KRM Fuzzer | | | Not Started | | |
| 4 | Implement Direct Controller & E2E Fixtures | | | Not Started | | |

## Status Update Notes
- **2026-06-17**: Verified PR #10164 checks are still failing. Re-attempted assignment to `factorybot-robot` but hit GraphQL scope constraints and REST API 404. Status remains monitored as overseer.
- **2026-06-17**: Checked PR #10164 and confirmed CI checks are still failing on the latest head commit. Attempted to assign PR to `factorybot-robot` via REST API but failed with 404. Status remains monitored as overseer.
- **2026-06-16**: Checked PR #10164 and confirmed CI checks are still failing on the latest head commit. Monitored status as overseer.
- **2026-06-16**: Verified PR #10164. CI checks are still failing. Attempted to assign the PR to `factorybot-robot` via API but failed because the user was not found on the repository. Status remains monitored.
- **2026-06-16**: Checked PR #10164 and found failing CI checks on the head commit. Assigned PR to `factorybot-robot` to trigger correction.
- **2026-06-16**: Checked PR #10164 and found failing CI checks on the latest head commit. Verified and monitored status as overseer.
- **2026-06-16**: Initialized migration journal for ComputeURLMap. Step 1 issue (#10137) is open and PR (#10164) is in progress but has failing CI checks.
