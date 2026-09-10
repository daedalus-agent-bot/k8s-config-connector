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
- Checked CI checks rollup for the latest commit (`74026f8`). Every single check run (out of 200+) has now passed successfully.
- Verified that the PR remains open. The automated system `argus-watcher-bot` is continuing to process and address the review feedback from `reviewbot-robot` in its sandbox environment. We remain in Step 1, waiting for the PR to be merged before starting Step 2.
- Checked CI status again on the latest commit (`74026f80455ca48b31080052b9497faa9d76ada6`). All checks have successfully passed! This includes previously failing `unit-tests-operator` and `unit-tests-2-of-4` checks, which were resolved by `ada-coder-bot` via generating golden files/exceptions and force-pushing.
- The PR received automated review feedback from `reviewbot-robot` detailing three findings: (1) change `Location` to a pointer string `*string`, (2) update copyright years to 2026 for new files, and (3) fix a typo in the error message for location resolution in identity.
- Automated system (`argus-watcher-bot`) has already launched a sandbox to address this review feedback. We remain in Step 1, waiting for the feedback to be addressed and the PR to be merged.
- Verified that Pull Request [#12870](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12870) has been created for Step 1.
- PR is currently open and CI checks are running. Some initial compilation issues were investigated and force-push resolved by `ada-coder-bot`.
- Checked the CI check-run status for the latest commit (`00fc3faf08f20f66476eac38f333d81a3b64a9aa`). While most of the 200+ checks passed, `unit-tests-operator` and `unit-tests-2-of-4` failed.
- Observed that `argus-watcher-bot` has automatically launched an investigation into these failures. We will wait for the CI checks to be resolved and the PR to be merged before starting Step 2.

### 2026-09-09
- Initialized greenfield migration for `CloudNumberRegistryIpamAdminScope`.
- Created GitHub issue [#12854](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12854) for Step 1.
- Checked status of Step 1. Issue [#12854](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12854) is open, and AI Factory sandbox development has started. No Pull Request has been created yet.
