# Migration Journal: IAPBrand

## Current Step
Step 4: Ensure MockGCP matches real gcp behavior

## Progress Tracking

| Step | Name | Issue | Pull Request | Status | Date Started | Date Completed |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Direct API Types | [Issue #10375](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10375) | [PR #10381](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10381) | Merged | 2026-06-16 | 2026-06-17 |
| 2 | Identity and Reference Types Pattern | [Issue #10392](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10392) | [PR #10394](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10394) | Merged | 2026-06-17 | 2026-06-18 |
| 3 | Create a Round-Trip KRM Fuzzer | [Issue #10478](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10478) | [PR #10479](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10479) | Merged | 2026-06-18 | 2026-06-19 |
| 4 | Ensure MockGCP matches real gcp behavior | [Issue #10485](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10485) | [PR #10502](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10502) | PR Created | 2026-06-19 | - |
| 5 | Implement Direct Controller & E2E Fixtures | - | - | - | - | - |

## Status Updates
- **2026-06-19**: Step 4 initiated. Issue #10485 opened and PRs #10502 (MockGCP alignment) and #10525 (normalization fix) created. E2E tests are under investigation and fix by the coder bot.
- **2026-06-20**: Verified all check-runs are complete. Active discussion on PR #10502 between `@barney-s` and the bots clarified that real GCP E2E recording for IAP Brand is blocked by the supportEmail constraint on headless Service Accounts. The PR was updated to use MockGCP as the source of truth and is awaiting human owner review and merging.
- **2026-06-21**: Conducted a progress audit of Step 4. Conclusively verified that parent Pull Request #10502 and child Pull Request #10525 both remain open but are completely 100% green, with all automated checks passing successfully with zero failures. We are actively awaiting human owner reviews, approval, and merging on the master branch before transitioning to Step 5.
