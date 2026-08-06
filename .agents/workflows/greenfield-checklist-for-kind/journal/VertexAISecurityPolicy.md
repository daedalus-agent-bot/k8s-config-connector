# Greenfield Migration Journal: VertexAISecurityPolicy

## Current Step
Step 1: Direct API Types and Identity and Reference Types Pattern

## Progress Tracking Table
| Step | Name | GitHub Issue | Pull Request | Status | Date Started | Date Completed |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Direct API Types and Identity | [#12012](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12012) | [#12041](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12041) | PR Created | 2026-07-29 | |
| 2 | Direct Controller and E2E Fixtures | | | | | |
| 3 | mockGCP Generation | | | | | |
| 4 | MockGCP Alignment | | | | | |

## Status Update Notes
- **2026-08-06**: Checked PR #12041 status. All 130+ CI checks continue to pass successfully, but the PR has been flagged as dirty with merge conflicts. Assigned the PR back to the author bot `neumann-coder-bot` to resolve the conflicts and rebase.
- **2026-08-06**: Checked PR #12041 status again. All 130+ CI checks continue to be completely green and passing. The PR remains open, awaiting human OWNER review, approval, and merge before we can proceed to Step 2.
- **2026-08-06**: Re-verified PR #12041 status. Checked CI check results and confirmed that all 130+ checks remain completely green and passing. The PR remains open and is awaiting human OWNER review, approval, and merge to complete Step 1.
- **2026-07-29**: Checked PR #12041 again. Verified all 201 CI check-runs continue to be 100% green and successful. The PR remains open, awaiting human OWNER review and merge to complete Step 1.
- **2026-07-29**: Monitored PR #12041. Re-verified that all 201 CI check-runs remain 100% green and successful. The PR is open, awaiting human OWNER review and merge to complete Step 1 before we can proceed to Step 2.
- **2026-07-29**: Re-verified PR #12041 status. All 130+ CI check-runs are now 100% green and passing (including unit-tests, linters, and e2e fixtures). The previous pluralization and golden file failures have been resolved. The PR remains open, awaiting human OWNER review and merge to complete Step 1.
- **2026-07-29**: Checked PR #12041 status again. Confirmed that all 130+ CI checks continue to be 100% green and passing. The PR remains open, awaiting human OWNER review and merge to complete Step 1.
- **2026-07-29**: Checked PR #12041 status again. All 130+ CI check-runs are completely green and passing. The PR remains open, awaiting human OWNER review, approval, and merge before we can proceed to Step 2.
- **2026-07-29**: Monitored PR #12041. All 130+ CI checks are passing successfully. No reviews or approvals have been submitted yet. The PR remains open, awaiting human OWNER review and merge before proceeding to Step 2.
- **2026-07-29**: Monitored PR #12041. Re-verified that all 130+ CI checks are fully complete and green. The PR remains open, awaiting human OWNER review, approval, and merge to complete Step 1.
- **2026-07-29**: Re-verified PR #12041 status. All 130+ CI check-runs are completely green and passing. The PR is still open and awaiting human OWNER review, approval, and merge.
- **2026-07-29**: Checked PR #12041. All 130+ CI checks (including validations, unit-tests, and e2e fixtures) are completely green and passing. The PR remains open, awaiting human OWNER review, approval, and merge before we can proceed to Step 2.
- **2026-07-29**: Monitored PR #12041. Checked CI checks status and verified all are green and passing. The PR is still open, waiting for human OWNER review and merge to complete Step 1.
- **2026-07-29**: Monitored PR #12041. Verified that all 130+ CI checks continue to pass successfully. The PR is open, awaiting human OWNER review, approval, and merge to complete Step 1.
- **2026-07-29**: Re-verified PR #12041 status. All 130+ CI check-runs (including unit-tests, linters, static validations, and e2e fixtures) are completely green and passing. The PR remains open, awaiting human OWNER review and merge to complete Step 1.
- **2026-07-29**: Re-checked PR #12041 status. All 130+ CI check-runs are completely green and passing. The PR remains open, awaiting human OWNER review, approval, and merge to complete Step 1.
- **2026-07-29**: Checked PR #12041 and confirmed that all 130+ CI check-runs continue to pass successfully with no errors. The PR remains open, awaiting human OWNER review and merge to complete Step 1.
- **2026-07-29**: Checked PR #12041 and verified that all 130+ CI check-runs are completely green and passing (including validations, unit-tests, and fixtures). The PR remains open, awaiting human OWNER review and merge to complete Step 1 before we can proceed to Step 2.
- **2026-07-29**: Checked PR #12041. All 130+ CI checks are fully complete and green. The PR remains open and is currently awaiting human OWNER review and merge to complete Step 1.
- **2026-07-29**: Re-verified PR #12041 status. All 130+ CI check-runs are completely green and passing. The PR remains open, awaiting human OWNER review and merge to complete Step 1.
- **2026-07-29**: Checked PR #12041 and confirmed that all 130+ CI checks continue to pass successfully. The PR remains open, awaiting human OWNER review and merge before we can proceed to Step 2.
- **2026-07-29**: Monitored PR #12041 and verified that all 130+ CI check-runs are clean and passing. The PR remains open, pending human review and merge to complete Step 1.
- **2026-07-29**: Re-checked PR #12041 and confirmed that all 130+ CI checks are successful. Verified that no reviewer comments or approvals have been posted yet. The PR remains open, awaiting human OWNER review and merge to complete Step 1.
- **2026-07-29**: Checked PR #12041 status and confirmed that all CI checks continue to pass successfully. The PR is still open and awaiting human OWNER review and merge before we can proceed to Step 2.
- **2026-07-29**: Verified that all completed CI check-runs for PR #12041 are now passing (including unit-tests, linters, static validations, and e2e fixtures checks). The PR is currently open and awaiting human OWNER approval and merge.
- **2026-07-29**: PR #12041 is open. Inspected the failing `unit-tests` check-run and identified that `TestCRDShortNamePluralization` failed because the plural shortName `gcpvertexaisecuritypolicys` is flagged as an incorrect pluralization of `gcpvertexaisecuritypolicy`. Noticed that `argus-watcher-bot` started investigating the CI failures on the PR, and `neumann-coder-bot` remains assigned to fix it.
- **2026-07-29**: PR #12041 was created by neumann-coder-bot. Checked CI results and found unit tests are failing. Assigned neumann-coder-bot to the PR to investigate and fix the unit-test failures.
- **2026-07-29**: Monitored Step 1 progress. Coder bot is still working on generating direct KRM types and identity for VertexAISecurityPolicy in the sandbox; no PR has been opened yet.
- **2026-07-29**: Step 1 is in progress. Issue [#12012](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12012) is assigned to the coder bot and sandbox work has begun.
- **2026-07-29**: Started migration for VertexAISecurityPolicy. Created Step 1 GitHub issue [#12012](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12012).
