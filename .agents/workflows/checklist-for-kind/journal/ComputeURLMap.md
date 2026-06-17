# Migration Journal: ComputeURLMap

## Current Step
Step 1: Direct API Types (In Progress - PR Created, CI Passed)

## Progress Tracking

| Step | Step Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
|---|---|---|---|---|---|---|
| 1 | Direct API Types | [#10137](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10137) | [#10164](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10164) | PR Created | 2026-06-13 | |
| 2 | Identity and Reference Types Pattern | | | Not Started | | |
| 3 | Create a Round-Trip KRM Fuzzer | | | Not Started | | |
| 4 | Implement Direct Controller & E2E Fixtures | | | Not Started | | |

## Status Update Notes
- **2026-06-17**: Verified PR #10164 remains open on head commit d4eec8f with all 176 CI check-runs passing successfully. Continuing to monitor as overseer, awaiting human review, OWNER approval, and merge.
- **2026-06-17**: Verified that PR #10164 remains fully clean on head commit d4eec8f with all 176 CI check-runs passing successfully. Continuing to monitor as overseer, awaiting human review and merge.
- **2026-06-17**: Checked PR #10164 status. Confirmed all 176 CI checks have successfully completed and passed. The PR remains open, awaiting human review, OWNER approval, and merge.
- **2026-06-17**: Verified that PR #10164 remains open with all 176 CI check-runs passing successfully. Continuing to monitor as overseer, awaiting human review and merge.
- **2026-06-17**: Checked PR #10164 on GitHub. Verified that all 176 CI check-runs are successfully passing. The PR remains open, awaiting human reviewer/OWNER approval and merge before the migration can proceed to Step 2.
- **2026-06-17**: Monitored PR #10164 and verified all 176 CI check-runs remain fully passing with zero failures. The PR is awaiting human reviewer/OWNER approval and merge before the migration can proceed to Step 2.
- **2026-06-17**: Checked PR #10164 status. Confirmed that the PR is still open, and all CI check-runs on the head commit d4eec8ffdbb80a4fbc6f8bfc38937e6a392ab55f have passed successfully. Awaiting human review and merge before proceeding to Step 2.
- **2026-06-17**: Verified that PR #10164 has completed all CI checks successfully with zero failures. The PR remains open and is awaiting human review and merge. Continuing to monitor as overseer.
- **2026-06-17**: Re-evaluated PR #10164 CI checks. Confirmed that all 176 check runs have completed successfully with zero failures. The PR remains open and is awaiting human review and merge. Status remains monitored as overseer.
- **2026-06-17**: Verified that PR #10164 continues to have all CI checks fully passing. The PR remains open, awaiting human review, OWNER approval, and merge. Status remains monitored.
- **2026-06-17**: Monitored PR #10164. Confirmed that all CI checks continue to pass successfully. The PR is awaiting human reviewer approval and merge. Status remains monitored as overseer.
- **2026-06-17**: Re-evaluated PR #10164. All CI checks, including all e2e-fixtures, have now completed and passed successfully. The PR is open and pending human review/merge. Status remains monitored as overseer.
- **2026-06-17**: Checked PR #10164 status on the head commit `d4eec8f`. All previously failing checks (such as `validate-generated-files`, `run-linters`, `golangci-lint`) have now completed and passed successfully. A few e2e-fixtures checks are still in progress/pending with no failures detected. Status remains monitored as overseer.
- **2026-06-17**: Checked PR #10164. Confirmed that on the head commit `d4eec8f`, all CI checks are currently running (in progress) with no failures detected so far. Status remains monitored.
- **2026-06-17**: Re-evaluated the CI checks for PR #10164 on the new head commit 912cc3ebddbfe0f766e83d4bfd8a760a3041a7f7. Confirmed that the `validate-generated-files` check is failing, while other CI checks are currently in progress. Successfully assigned the PR to `codebot-robot` to trigger automatic correction. Status remains monitored.
- **2026-06-17**: Re-evaluated the CI checks for PR #10164. Confirmed that multiple checks (such as build-images, fuzz-roundtrippers, golangci-lint, run-linters, test-pause, tests-gcptracker, tests-preview, unit-tests, and validate-generated-files) continue to fail on head commit b088d8ce7a34ef00ba135fc21990554482bdec2f. Status remains monitored as overseer.
- **2026-06-17**: Checked PR #10164 and confirmed CI checks are still failing. Added `direct-migration` and `overseer` labels to the PR, and successfully assigned it to `codebot-robot` to trigger auto-correction/action. Status remains monitored as overseer.
- **2026-06-17**: Verified PR #10164 checks are still failing on head commit b088d8ce7a34ef00ba135fc21990554482bdec2f. Attempted to assign PR to `factorybot-robot` via REST API to trigger auto-correction, but assignment was not permitted (HTTP 404). Status remains monitored as overseer.
- **2026-06-17**: Checked PR #10164 and confirmed CI checks are still failing. Successfully assigned the PR to `daedalus-agent-bot` to track progress. Status remains monitored as overseer.
- **2026-06-17**: Verified PR #10164 checks are still failing. Re-attempted assignment to `factorybot-robot` but hit GraphQL scope constraints and REST API 404. Status remains monitored as overseer.
- **2026-06-17**: Checked PR #10164 and confirmed CI checks are still failing on the latest head commit. Attempted to assign PR to `factorybot-robot` via REST API but failed with 404. Status remains monitored as overseer.
- **2026-06-16**: Checked PR #10164 and confirmed CI checks are still failing on the latest head commit. Monitored status as overseer.
- **2026-06-16**: Verified PR #10164. CI checks are still failing. Attempted to assign the PR to `factorybot-robot` via API but failed because the user was not found on the repository. Status remains monitored.
- **2026-06-16**: Checked PR #10164 and found failing CI checks on the head commit. Assigned PR to `factorybot-robot` to trigger correction.
- **2026-06-16**: Checked PR #10164 and found failing CI checks on the latest head commit. Verified and monitored status as overseer.
- **2026-06-16**: Initialized migration journal for ComputeURLMap. Step 1 issue (#10137) is open and PR (#10164) is in progress but has failing CI checks.
