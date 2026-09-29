# Migration Journal: OracleDatabaseExadbVMCluster

## Current Step
Step 2: Direct Controller, E2E fixtures and Fuzzer

## Progress Tracking

| Step Number & Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
| --- | --- | --- | --- | --- | --- |
| 1. Direct API Types, Identity, and generate.sh | [#13321](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/13321) | [#13339](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/13339), [#13415](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/13415) | PR Created | 2026-09-19 | N/A |
| 2. Direct Controller, E2E fixtures, and Fuzzer | [#13370](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/13370) | [#13376](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/13376) | PR Created | 2026-09-23 | N/A |
| 3. mockGCP generation | N/A | N/A | Pending | N/A | N/A |
| 4. MockGCP Alignment with RealGCP | N/A | N/A | Pending | N/A | N/A |

## Status Update Log

- **2026-09-29**: Recorded follow-up Pull Request [#13415](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/13415) for Step 1 (updating reference types to be external-only). Both Step 1 PR [#13415](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/13415) and Step 2 PR [#13376](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/13376) have passed all CI checks and are labeled `overseer/ready-for-human`, awaiting review and merge.
- **2026-09-29**: Pull Request [#13376](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/13376) for Step 2 passed all CI checks and is labeled `overseer/ready-for-human`, awaiting review and merge.
- **2026-09-28**: Pull Request [#13376](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/13376) created for Step 2 (Direct Controller, E2E fixtures, and Fuzzer). Monitoring PR progress.
- **2026-09-23**: Step 1 completed with the merging of PR [#13339](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/13339). Created GitHub Issue [#13370](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/13370) for Step 2 (Direct Controller, E2E fixtures, and Fuzzer).
- **2026-09-19**: Initiated the Greenfield migration orchestration. Created GitHub Issue [#13321](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/13321) for Step 1 (Direct API Types, Identity, and generate.sh).
