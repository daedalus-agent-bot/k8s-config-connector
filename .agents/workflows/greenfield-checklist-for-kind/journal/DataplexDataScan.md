# Greenfield Migration Journal: DataplexDataScan

**Current Step:** Step 4: MockGCP Alignment with RealGCP

## Progress Tracking

| Step | Step Name | GitHub Issue | GitHub PR | Status | Date Started | Date Completed |
|------|-----------|--------------|-----------|--------|--------------|----------------|
| 1 | Direct API Types and Identity | [#8681](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/8681) | [#8693](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/8693) | Merged | 2026-06-21 | 2026-06-21 |
| 2 | Direct Controller, E2E fixtures, Fuzzer | [#13235](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/13235) | [#13278](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/13278) | Merged | 2026-09-18 | 2026-10-29 |
| 3 | mockGCP generation | [#14614](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14614) | [#14628](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14628) | Merged | 2026-10-29 | 2026-10-30 |
| 4 | MockGCP Alignment with RealGCP | [#14692](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14692) | N/A | Open | 2026-10-30 | N/A |

## Notes & Status Updates

* **2026-10-30:** Step 3 completed (PR #14628 merged). Opened Step 4 issue #14692 to align MockGCP logs with RealGCP for `DataplexDataScan`.
* **2026-10-29:** PR #14628 created for Step 3 (MockGCP and Alignment for `DataplexDataScan`). Waiting for PR review and merge before proceeding to Step 4.
* **2026-10-29:** Step 2 completed (PR #13278 merged). Opened Step 3 issue #14614 to implement MockGCP and Alignment for `DataplexDataScan`.
* **2026-09-28:** PR #13278 created for Step 2 (Direct Controller, E2E fixtures, and fuzzer). Waiting for PR review and merge before proceeding to Step 3.
* **2026-09-18:** Started Greenfield migration tracking for `DataplexDataScan`. Verified that Step 1 (API Types & Identity) was already completed in issue #8681 / PR #8693. Opened Step 2 issue (#13235) to implement direct controller, E2E fixtures, and fuzzer.
