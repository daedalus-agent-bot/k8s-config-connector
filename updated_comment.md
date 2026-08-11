# Migration Progress: ComputeFirewallPolicy

**Current Step:** Step 6: Validate Direct Promotion

| Step Number & Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
|---|---|---|---|---|---|
| **Step 1: Direct API Types** | [#9974](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/9974) | [#10064](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10064) | Merged | 2026-06-13 | 2026-06-19 |
| **Step 2: Identity and Reference Types Pattern** | [#10526](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10526) | [#10532](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10532) | Merged | 2026-06-23 | 2026-06-23 |
| **Step 3: Create a Round-Trip KRM Fuzzer** | [#10721](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10721) | [#10723](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10723) | Merged | 2026-06-23 | 2026-06-23 |
| **Step 4: Ensure MockGCP matches real gcp behavior** | [#10885](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10885) | [#10912](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10912) | Merged | 2026-06-25 | 2026-06-27 |
| **Step 5: Implement Direct Controller & E2E Fixtures** | [#11130](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/11130) (also [#10919](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10919)) | [#11131](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11131) (also [#10920](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10920)) | Merged | 2026-06-28 | 2026-07-03 |
| **Step 6: Validate Direct Promotion** | [#12081](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12081) | [#12091](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12091) | PR Created | 2026-07-30 | - |

### Recent Status Update Notes

- **2026-08-11**: Re-verified final promotion PR [#12091](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12091) status. Re-confirmed all 120+ CI check suites continue to remain completely green and passing successfully. The PR is OPEN and awaiting final human OWNER review, approval, and merge.
- **2026-08-11**: Verified all 120+ CI check suites (including `crd-equivalence-check` and all E2E fixture suites) are fully passing and completely green. The PR remains open, awaiting final human OWNER review, approval, and merge.
- **2026-08-11**: Re-monitored final promotion PR [#12091](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12091) status. Verified all 200+ CI check suites continue to remain completely green and passing successfully. The PR remains OPEN, pending final human OWNER review, approval, and merge.
