# Greenfield Migration Progress: AIPlatformSpecialistPool

Parent Issue: [#12838](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12838)

## Current Status
Currently on **Step 1**: Implement direct KRM types, identity, and generate.sh for AIPlatformSpecialistPool.

## Progress Table
| Step | Description | GitHub Issue | GitHub PR | Status | Date Started | Date Completed |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Direct KRM types, identity, and generate.sh | [#12846](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12846) | [#12857](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12857) | Awaiting Review | 2026-09-09 | - |
| 2 | Direct controller, E2E fixtures, and fuzzer | - | - | Pending | - | - |
| 3 | mockGCP generation | - | - | Pending | - | - |
| 4 | MockGCP Alignment with RealGCP | - | - | Pending | - | - |

## Step Notes & Updates
- **2026-09-10**: Addressed PR review feedback regarding Go Type Pointers. Hopper-coder-bot converted `Location` and `DisplayName` fields in `AIPlatformSpecialistPoolSpec` to pointer types (`*string`), deleted the redundant custom mapper, and successfully regenerated all clientsets and manifests. All GitHub Actions CI checks have successfully passed on the latest commit. The PR is open and awaiting maintainer review/merge.
- **2026-09-10**: Verified PR [#12857](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12857). All CI checks have now successfully passed. The PR is open and awaiting maintainer review.
- **2026-09-10**: Verified PR [#12857](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12857). Found that the CI check `unit-tests-4-of-4` is currently failing due to grammatical grammar-check error (`unexpected diff in testdata/exceptions/comments.txt` indicating 'a AIPlatformSpecialistPool' should be 'an AIPlatformSpecialistPool'). Argus/coder bots are currently investigating/fixing this in the sandbox. Waiting for Step 1 PR to compile, pass all CI checks, and merge.
- **2026-09-09**: PR [#12857](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12857) was opened for Step 1 by hopper-coder-bot. Verified PR state and CI check-runs.
- **2026-09-09**: Initialized the migration checklist. Step 1 child issue created: [#12846](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12846).
