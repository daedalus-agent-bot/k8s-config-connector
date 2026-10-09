# Migration Journal: FirebaseHostingSite

## Current Step
Step 3: Create a Round-Trip KRM Fuzzer

## Progress Tracking

| Step | Name | Issue | PR | Status | Date Started | Date Completed |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Direct API Types | [#13817](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/13817) | [#13823](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/13823) | Completed | 2026-10-08 | 2026-10-09 |
| 2 | Identity and Reference Types Pattern | - | [#13823](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/13823) | Completed | 2026-10-08 | 2026-10-09 |
| 3 | Create a Round-Trip KRM Fuzzer | [#13878](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/13878) | - | Open | 2026-10-09 | - |
| 4 | Ensure MockGCP matches real gcp behavior | - | - | Pending | - | - |
| 5 | Implement Direct Controller & E2E Fixtures | - | - | Pending | - | - |
| 6 | Validate Direct Promotion | - | - | Pending | - | - |

## Status Update Notes
- **2026-10-08**: Migration initialized for FirebaseHostingSite. Created Step 1 child issue #13817 to scaffold direct KRM types and generate.sh.
- **2026-10-09**: Step 1 & 2 completed via PR #13823 (merged), providing direct KRM types, generate.sh, and IdentityV2/Ref patterns.
- **2026-10-09**: Created Step 3 child issue #13878 to implement round-trip KRM fuzzer for FirebaseHostingSite.
