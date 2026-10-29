# Migration Journal: BeyondCorpAppConnection

## Current Step
Step 4: Ensure MockGCP matches real gcp behavior

## Progress Tracking

| Step Number and Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
|---|---|---|---|---|---|
| Step 1: Direct API Types | [#14351](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14351) | [#14375](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14375) | Merged | 2026-10-23 | 2026-10-28 |
| Step 2: Identity and Reference Types Pattern | [#14501](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14501) | [#14503](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14503) | Merged | 2026-10-28 | 2026-10-28 |
| Step 3: Create a Round-Trip KRM Fuzzer | [#14512](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14512) | [#14514](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14514) | Merged | 2026-10-28 | 2026-10-29 |
| Step 4: Ensure MockGCP matches real gcp behavior | [#14551](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14551) | - | Open | 2026-10-29 | - |
| Step 5: Implement Direct Controller & E2E Fixtures | - | - | Pending | - | - |
| Step 6: Validate Direct Promotion | - | - | Pending | - | - |

## History and Notes
- **2026-10-29**: Created Step 4 child issue [#14551](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14551) assigned to `factorybot-robot` to match real GCP behavior in MockGCP for BeyondCorpAppConnection.
- **2026-10-29**: Step 3 PR [#14514](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14514) merged. Completed Step 3: Create a Round-Trip KRM Fuzzer.
- **2026-10-28**: Pull Request [#14514](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14514) opened for Step 3 child issue [#14512](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14512). CI presubmit checks running.
- **2026-10-28**: Created Step 3 child issue [#14512](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14512) to implement round-trip KRM fuzzer for BeyondCorpAppConnection.
- **2026-10-28**: Step 2 PR [#14503](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14503) merged. Completed Step 2: Identity and Reference Types Pattern.
- **2026-10-28**: Pull Request [#14503](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14503) opened for Step 2 child issue [#14501](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14501). All CI presubmit checks passed, reviewed (`overseer/ready-for-human`); awaiting approval and merge.
- **2026-10-28**: Step 1 PR [#14375](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14375) merged. Proceeded to Step 2; tracking existing child issue [#14501](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14501) assigned to lovelace-coder-bot.
- **2026-10-24**: Pull Request [#14375](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14375) created for Step 1 issue [#14351](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14351). Awaiting CI checks and review completion.
- **2026-10-23**: Migration workflow initialized for BeyondCorpAppConnection. Created child issue [#14351](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14351) for Step 1: Direct API Types.
