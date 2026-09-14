# Greenfield Migration Checklist: RunWorkerPool

Current Step: Step 2: Direct Controller, E2E fixtures and Fuzzer

| Step | Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
|------|------|--------------|---------------------|--------|--------------|----------------|
| 1    | Direct API Types, Identity & Refs | [#12912](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12912) | [#12914](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12914) | Completed | 2026-09-11 | 2026-09-14 |
| 2    | Direct Controller, E2E fixtures & Fuzzer | [#12927](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12927) | | Open | 2026-09-14 | |
| 3    | mockGCP generation | | | Pending | | |
| 4    | MockGCP Alignment with RealGCP | | | Pending | | |

## Status Updates
- **2026-09-14**: Pull request #12914 was successfully merged. Successfully completed Step 1. Created child issue #12927 to track Step 2 (Direct Controller, E2E fixtures & Fuzzer).
- **2026-09-11**: Pull request #12914 was created, and all CI checks have passed successfully. Waiting for maintainer review and merge.
- **2026-09-11**: Started greenfield migration checklist. Types and mapper were previously merged in PR #7246, but identity, reference, and generate.sh configuration for RunWorkerPool are still missing or incomplete. Created GitHub child issue #12912 to track Step 1 completion.
