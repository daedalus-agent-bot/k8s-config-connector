# Migration Journal: IAPBrand

## Current Step
Step 1: Direct API Types

## Progress Tracking

| Step | Name | Issue | Pull Request | Status | Date Started | Date Completed |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Direct API Types | [Issue #10375](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10375) | [PR #10381](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10381) | PR Created | 2026-06-16 | - |
| 2 | Identity and Reference Types Pattern | - | - | - | - | - |
| 3 | Create a Round-Trip KRM Fuzzer | - | - | - | - | - |
| 4 | Implement Direct Controller & E2E Fixtures | - | - | - | - | - |

## Status Updates
- **2026-06-17**: Checked progress on PR #10381. The PR remains open but blocked by failing CI checks (`unit-tests` and `validations`). Step 1 remains in progress.
- **2026-06-17**: PR #10379, PR #10384, and PR #10385 were closed. PR #10381 remains the primary open PR for Step 1.
- **2026-06-17**: Opened Pull Request #10379 and Pull Request #10381 with the `overseer` label to address Issue #10375. Both PRs were initially failing CI checks due to `validate-generated-files` (out-of-date `apis/cloudbuild/v1alpha1/types.generated.go`) and `unit-tests` (infrastructure authentication issue). Code compiles and passes local validation checks.
- **2026-06-16**: Started migration for IAPBrand. Opened Issue #10375 to implement direct KRM types and generate.sh for IAPBrand.
