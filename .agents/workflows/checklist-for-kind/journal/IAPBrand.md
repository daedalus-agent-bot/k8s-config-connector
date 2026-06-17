# Migration Journal: IAPBrand

## Current Step
Step 2: Identity and Reference Types Pattern

## Progress Tracking

| Step | Name | Issue | Pull Request | Status | Date Started | Date Completed |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Direct API Types | [Issue #10375](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10375) | [PR #10381](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10381) | PR Created | 2026-06-16 | - |
| 2 | Identity and Reference Types Pattern | [Issue #10392](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10392) | [PR #10393](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10393), [PR #10394](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10394) | PR Created | 2026-06-17 | - |
| 3 | Create a Round-Trip KRM Fuzzer | - | - | - | - | - |
| 4 | Implement Direct Controller & E2E Fixtures | - | - | - | - | - |

## Status Updates
- **2026-06-17**: Re-verified that both Pull Request #10381 (Step 1) and Pull Request #10394 (Step 2) are open and 100% green on GitHub with all automated CI check-runs passing successfully. We continue to await human maintainer review, approval, and merge of both PRs before we can proceed to Step 3 (Create a Round-Trip KRM Fuzzer).
- **2026-06-17**: Re-checked the statuses of PR #10381 (Step 1) and PR #10394 (Step 2). Both PRs remain open and are passing all of their automated CI checks (100% green). We must wait for human owner review and merging of these PRs before we can proceed to Step 3 (Create a Round-Trip KRM Fuzzer).
- **2026-06-17**: Monitored open Pull Requests. Verified that PR #10381 (Step 1) and PR #10394 (Step 2) remain open and 100% green on GitHub with all CI checks passing successfully. PR #10393 is open but failing, leaving PR #10394 as the healthy PR for Step 2. We continue to await human owner review, approval, and merge of the Step 1 PR before we can transition to Step 3.
- **2026-06-17**: Re-verified both open Pull Requests #10381 (Step 1) and #10394 (Step 2). Both remain open and 100% green on GitHub, passing all automated CI checks. We continue to await human owner review, approval, and merge of both PRs before we can transition to Step 3 (Create a Round-Trip KRM Fuzzer).
- **2026-06-17**: Re-checked the status of PR #10381 (Step 1) and PR #10394 (Step 2). Both PRs are open and fully green, passing all automated CI check-runs. We continue to await human review, approval, and merging of these PRs on the upstream repository before we can proceed to Step 3 (Create a Round-Trip KRM Fuzzer).
- **2026-06-17**: Re-monitored both Pull Request #10381 (Step 1) and Pull Request #10394 (Step 2) on GitHub. Confirmed both remain open and 100% green, passing all CI checks successfully. We continue to await human maintainer review, approval, and merge of both PRs before we can transition to Step 3 (Create a Round-Trip KRM Fuzzer).
- **2026-06-17**: Verified that both Pull Request #10381 (Step 1) and Pull Request #10394 (Step 2) are open and all of their CI checks have successfully passed (100% green on GitHub). We are awaiting human owner review, approval, and merge of both PRs before we can proceed to Step 3 (Create a Round-Trip KRM Fuzzer).
- **2026-06-17**: Re-monitored the status of both open PRs. Confirmed that PR #10381 (Step 1) and PR #10394 (Step 2) remain open and are passing all CI check-runs on the upstream repository. We must continue to wait for Step 1 and Step 2 PRs to be merged before initiating Step 3 (Create a Round-Trip KRM Fuzzer).
- **2026-06-17**: Re-verified the status of both open PRs. PR #10381 (Step 1) and PR #10394 (Step 2) are both passing all CI check-runs but remain open. Since Step 1 has not been merged, we cannot proceed to Step 3. We are monitoring both PRs for owner approval and merging.
- **2026-06-17**: Verified that all CI checks for Pull Request #10394 (Step 2) have successfully passed and are 100% green on GitHub. Both Pull Request #10381 (Step 1) and Pull Request #10394 (Step 2) are now fully validated and awaiting human owner review, approval, and merge. We must wait for these PRs to be merged before we can proceed to Step 3 (Create a Round-Trip KRM Fuzzer).
- **2026-06-17**: Verified that all CI checks for both Pull Request #10381 (Step 1) and Pull Request #10394 (Step 2) have successfully passed and are 100% green on GitHub. Both PRs are currently awaiting human owner review, approval, and merge on the upstream repository. We must wait for these PRs to be merged before we can proceed to Step 3 (Create a Round-Trip KRM Fuzzer).
- **2026-06-17**: Monitored progress of Step 2 ("Move IAPBrand to identity and refs pattern"). Verified that Pull Request #10394 remains open and active on GitHub. The CI check-runs on the latest commit `33ba8335d6` are currently in progress. We must continue to wait for all validations to pass and for the PR to be merged before starting Step 3 (Round-Trip KRM Fuzzer).
- **2026-06-17**: Re-checked progress of Step 2 ("Move IAPBrand to identity and refs pattern"). Found that PR #10394 was open but failing CI unit-tests because of a grammar check on the comment "a IAPBrand" (which starts with a vowel sound). Modified `apis/iap/v1beta1/iapbrand_reference.go` to change "a IAPBrand" to "an IAPBrand" for Name and Namespace fields, and verified that the entire local unit-test suite (`go test ./tests/apichecks/...`) now passes flawlessly. Awaiting automated PR validation of the fix.
- **2026-06-17**: Checked progress on PR #10381. The PR remains open but blocked by failing CI checks (`unit-tests` and `validations`). Step 1 remains in progress.
- **2026-06-17**: PR #10379, PR #10384, and PR #10385 were closed. PR #10381 remains the primary open PR for Step 1.
- **2026-06-17**: Opened Pull Request #10379 and Pull Request #10381 with the `overseer` label to address Issue #10375. Both PRs were initially failing CI checks due to `validate-generated-files` (out-of-date `apis/cloudbuild/v1alpha1/types.generated.go`) and `unit-tests` (infrastructure authentication issue). Code compiles and passes local validation checks.
- **2026-06-16**: Started migration for IAPBrand. Opened Issue #10375 to implement direct KRM types and generate.sh for IAPBrand.
