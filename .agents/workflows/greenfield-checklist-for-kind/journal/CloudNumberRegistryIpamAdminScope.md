# CloudNumberRegistryIpamAdminScope Greenfield Migration Journal

**Current Step:** Step 1: Direct API Types and Identity and Reference Types Pattern

| Step | Name | Issue | Pull Request | Status | Date Started | Date Completed |
|---|---|---|---|---|---|---|
| 1 | Direct API Types and Identity and Reference Types Pattern | [#12854](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12854) | [#12870](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12870) | PR Created | 2026-09-09 | - |
| 2 | Direct Controller, E2E fixtures and Fuzzer | - | - | Pending | - | - |
| 3 | mockGCP generation | - | - | Pending | - | - |
| 4 | MockGCP Alignment with RealGCP | - | - | Pending | - | - |

## Updates

### 2026-09-10
- Verified that Pull Request [#12870](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12870) has been created for Step 1.
- PR is currently open and CI checks are running. Some initial compilation issues were investigated and force-push resolved by `ada-coder-bot`.
- Checked the CI check-run status for the latest commit (`00fc3faf08f20f66476eac38f333d81a3b64a9aa`). While most of the 200+ checks passed, `unit-tests-operator` and `unit-tests-2-of-4` failed.
- Observed that `argus-watcher-bot` has automatically launched an investigation into these failures. We will wait for the CI checks to be resolved and the PR to be merged before starting Step 2.

### 2026-09-09
- Initialized greenfield migration for `CloudNumberRegistryIpamAdminScope`.
- Created GitHub issue [#12854](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12854) for Step 1.
- Checked status of Step 1. Issue [#12854](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12854) is open, and AI Factory sandbox development has started. No Pull Request has been created yet.
