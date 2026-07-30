# Migration Journal: ComputeMachineImage

This journal tracks the migration of `ComputeMachineImage` to a production-ready direct controller.

## Current Status
**Current Step:** Step 2: Move ComputeMachineImage to identity and refs pattern

## Progress Tracking

| Step | Step Name | GitHub Issue | GitHub PR | Status | Date Started | Date Completed |
|------|-----------|--------------|-----------|--------|--------------|----------------|
| 1 | Direct API Types | [#9991](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/9991) | [#10077](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10077) | Merged | 2026-07-06 | 2026-07-06 |
| 2 | Move ComputeMachineImage to identity and refs pattern | [#12076](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12076) | [#12084](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12084) | PR Created | 2026-07-29 | N/A |
| 3 | Implement round-trip KRM fuzzer | N/A | N/A | Pending | N/A | N/A |
| 4 | Match real gcp behavior in MockGCP | N/A | N/A | Pending | N/A | N/A |
| 5 | Implement direct controller and test fixtures | N/A | N/A | Pending | N/A | N/A |
| 6 | Validate direct promotion | N/A | N/A | Pending | N/A | N/A |

## History of Updates
- **2026-07-30 11:33 UTC**: Verified that PR #12084 has passed all 30 CI validation checks. The PR remains open and is awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-07-30**: PR #12084 was created by `ada-coder-bot` for Step 2. All CI validation checks have successfully passed. Awaiting human OWNER review and merge.
- **2026-07-30**: AI Factory (`ada-coder-bot`) has started implementing the identity and refs pattern for `ComputeMachineImage` (Issue #12076).
- **2026-07-29**: Step 1 is already completed and merged. Initiated Step 2 by creating GitHub Issue #12076 and assigning to `daedalus-agent-bot`.
