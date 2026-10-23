# Greenfield Migration Checklist: RunWorkerPool

Current Step: Step 4: MockGCP Alignment with RealGCP

| Step | Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
|------|------|--------------|---------------------|--------|--------------|----------------|
| 1    | Direct API Types, Identity & Refs | [#12912](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12912) | [#12914](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12914) | Completed | 2026-09-11 | 2026-09-14 |
| 2    | Direct Controller, E2E fixtures & Fuzzer | [#12927](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12927) | [#12928](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12928) | Completed | 2026-09-14 | 2026-10-23 |
| 3    | mockGCP generation | [#14303](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14303) | [#12928](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12928) | Completed | 2026-10-23 | 2026-10-23 |
| 4    | MockGCP Alignment with RealGCP | [#14307](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14307) | [#14308](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14308) | PR Created | 2026-10-23 | |

## Status Updates
- **2026-10-23**: Pull request [#14308](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14308) was created for Step 4 (MockGCP Alignment with RealGCP). All CI checks passed; awaiting review and merge.
- **2026-10-23**: Step 3 completed (MockGCP support implemented and verified in PR [#12928](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12928); child issue [#14303](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14303) closed). Opened child issue [#14307](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14307) to track Step 4 (MockGCP Alignment with RealGCP).
- **2026-10-23**: Pull request #12928 was merged. Completed Step 2. Opened child issue #14303 to track Step 3 (mockGCP generation).
- **2026-09-28**: Pull request #12928 is open and undergoing maintainer review for Step 2 (Direct Controller, E2E fixtures & Fuzzer). Waiting for merge before proceeding to Step 3.
- **2026-09-14**: Pull request #12928 was created for Step 2 (Direct Controller, E2E fixtures & Fuzzer).
- **2026-09-14**: Pull request #12914 was successfully merged. Successfully completed Step 1. Created child issue #12927 to track Step 2 (Direct Controller, E2E fixtures & Fuzzer).
- **2026-09-11**: Pull request #12914 was created, and all CI checks have passed successfully. Waiting for maintainer review and merge.
- **2026-09-11**: Started greenfield migration checklist. Types and mapper were previously merged in PR #7246, but identity, reference, and generate.sh configuration for RunWorkerPool are still missing or incomplete. Created GitHub child issue #12912 to track Step 1 completion.
