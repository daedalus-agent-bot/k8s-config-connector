# Greenfield Migration Journal: GKEBackupRestoreChannel

## Current Step: Step 4: Align MockGCP logs with RealGCP

| Step Number | Step Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Direct KRM types, identity, and generate.sh | [Issue #13317](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/13317) | [PR #13327](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/13327) | Merged | 2026-09-19 | 2026-10-16 |
| 2 | Direct controller, E2E fixtures, and fuzzer | [Issue #14049](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14049) | [PR #14067](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14067) | Merged | 2026-10-16 | 2026-10-24 |
| 3 | MockGCP and Alignment | [Issue #14384](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14384) | [PR #14406](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14406) | Merged | 2026-10-24 | 2026-10-27 |
| 4 | Align MockGCP logs with RealGCP | [Issue #14492](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14492) | - | Open | 2026-10-27 | - |

## Status Update Notes
- **2026-09-28**: PR #13327 created for Step 1, currently open and undergoing review.
- **2026-10-16**: Step 1 PR #13327 merged. Step 1 completed.
- **2026-10-16**: Started Step 2. Created child issue #14049 for direct controller, E2E fixtures, and fuzzer.
- **2026-10-17**: PR #14056 was closed without merging. Replaced by PR #14065 for Step 2.
- **2026-10-17**: Latest PR #14067 open for Step 2 (alongside PR #14065), currently undergoing review.
- **2026-10-24**: Step 2 PR #14067 merged. Step 2 completed.
- **2026-10-24**: Started Step 3. Created child issue #14384 for MockGCP and alignment.
- **2026-10-24**: PR #14406 created for Step 3, currently open and undergoing review.
- **2026-10-27**: Step 3 PR #14406 merged. Step 3 completed.
- **2026-10-27**: Started Step 4. Created child issue #14492 for aligning MockGCP logs with RealGCP.
