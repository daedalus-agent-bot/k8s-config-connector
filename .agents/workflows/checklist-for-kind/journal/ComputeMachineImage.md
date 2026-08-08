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
- **2026-08-08 17:23 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-08 13:52 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-08 10:19 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-08 06:04 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-08 00:15 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-07 21:00 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-07 17:51 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-07 14:49 UTC**: Re-verified PR #12084. All CI checks remain green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-07 11:44 UTC**: Re-verified PR #12084. All 136 CI check-runs remain green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-07 08:27 UTC**: Checked PR #12084. All 136 CI check-runs remain green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-05 22:25 UTC**: Checked PR #12084. All 136 CI check-runs are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-05 19:58 UTC**: Re-verified PR #12084. All 136 CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-05 17:32 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-05 15:09 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-05 12:59 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-05 10:21 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-05 07:50 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-05 05:18 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-05 02:49 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-05 00:16 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-04 21:36 UTC**: Re-verified PR #12084. All 136 CI check runs have successfully passed and are completely green. The PR remains open, awaiting human OWNER review and merge. Progress remains at Step 2.
- **2026-08-04 19:02 UTC**: Re-verified PR #12084. All 136 CI check runs have successfully passed and are completely green. The PR remains open, awaiting human OWNER review and merge. Progress remains at Step 2.
- **2026-08-04 16:21 UTC**: Re-verified PR #12084. All 136 CI check runs have successfully passed and are completely green. The PR remains open, awaiting human OWNER review and merge. Progress remains at Step 2.
- **2026-08-04 13:30 UTC**: Re-verified PR #12084. All 136 CI check runs have successfully passed and are completely green. The PR remains open, awaiting human OWNER review and merge. Progress remains at Step 2.
- **2026-08-04 10:46 UTC**: Re-verified PR #12084. All 136 CI check runs have successfully passed and are completely green. The PR remains open, awaiting human OWNER review and merge. Progress remains at Step 2.
- **2026-08-04 08:05 UTC**: Re-verified PR #12084. All 136 CI check runs have successfully passed and are completely green. The PR remains open, awaiting human OWNER review and merge. Progress remains at Step 2.
- **2026-08-04 05:13 UTC**: Re-verified PR #12084. All 136 CI check runs have successfully passed and are completely green. The PR remains open, awaiting human OWNER review and merge. Progress remains at Step 2.
- **2026-08-04 02:40 UTC**: Re-verified PR #12084. All 136 CI check runs have successfully passed and are completely green. The PR remains open, awaiting human OWNER review and merge. Progress remains at Step 2.
- **2026-08-03 23:57 UTC**: Re-verified PR #12084. All 136 CI check runs have successfully passed and are completely green. The PR remains open, awaiting human OWNER review and merge. Progress remains at Step 2.
- **2026-08-03 21:11 UTC**: Re-verified PR #12084. All 136 CI check runs have successfully passed and are completely green. The PR remains open, awaiting human OWNER review and merge. Progress remains at Step 2.
- **2026-08-03 18:18 UTC**: Re-verified PR #12084. All 136 CI check runs have successfully passed and are completely green. The PR remains open, awaiting human OWNER review and merge. Progress remains at Step 2.
- **2026-08-03 15:20 UTC**: Re-verified PR #12084. All 136 CI check runs have successfully passed and are completely green. The PR remains open, awaiting human OWNER review and merge. Progress remains at Step 2.
- **2026-08-03 13:06 UTC**: Re-verified PR #12084. All 136 CI check runs have successfully passed and are completely green. The PR remains open, awaiting human OWNER review and merge. Progress remains at Step 2.
- **2026-08-03 10:13 UTC**: Re-verified PR #12084. All 136 CI check runs have successfully passed and are completely green. The PR remains open, awaiting human OWNER review and merge. Progress remains at Step 2.
- **2026-08-03 07:22 UTC**: Re-verified PR #12084. All 136 CI check runs have successfully passed and are completely green. The PR remains open, awaiting human OWNER review and merge. Progress remains at Step 2.
- **2026-08-03 04:39 UTC**: Re-verified PR #12084. All 136 CI check runs have successfully passed and are completely green. The PR remains open, awaiting human OWNER review and merge. Progress remains at Step 2.
- **2026-08-03 02:03 UTC**: Re-verified PR #12084. All 136 CI check runs have successfully passed and are completely green. The PR remains open, awaiting human OWNER review and merge. Progress remains at Step 2.
- **2026-08-02 23:23 UTC**: Re-verified PR #12084. All 136 CI check runs have successfully passed and are completely green. The PR is open, awaiting human OWNER review and merge. Progress remains at Step 2.
- **2026-08-02 20:47 UTC**: Re-verified PR #12084. All 136 CI check runs have successfully passed. The PR is open, awaiting human OWNER review and merge. Progress remains at Step 2.
- **2026-08-02 18:08 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-02 15:34 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-02 12:58 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-02 10:26 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-02 07:41 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-02 04:41 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-02 02:00 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-01 23:19 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-01 20:46 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-01 18:03 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-01 15:20 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-01 12:34 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-01 09:43 UTC**: Re-verified PR #12084. All CI checks remain green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-01 07:07 UTC**: Re-verified PR #12084. All CI checks remain green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-01 04:21 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-08-01 01:25 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-07-31 22:54 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-07-31 19:57 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-07-31 17:02 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-07-31 14:30 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-07-31 13:35 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-07-31 10:58 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-07-31 08:30 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-07-31 05:22 UTC**: Verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-07-31 03:00 UTC**: Re-verified PR #12084. All CI checks are green (passing). The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-07-30 23:59 UTC**: Re-verified PR #12084. All CI checks are green. The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-07-30 21:06 UTC**: Re-verified PR #12084. All CI checks are green. The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-07-30 18:48 UTC**: Re-verified PR #12084. All CI checks are green. The PR remains open, awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-07-30 16:26 UTC**: Re-verified all CI checks for PR #12084. All checks are passing successfully. The PR remains open and is awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-07-30 13:53 UTC**: Verified that PR #12084 has successfully completed all CI checks. The PR remains open and is awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-07-30 11:33 UTC**: Verified that PR #12084 has passed all 30 CI validation checks. The PR remains open and is awaiting manual review and merge from a human OWNER. Progress remains at Step 2.
- **2026-07-30**: PR #12084 was created by `ada-coder-bot` for Step 2. All CI validation checks have successfully passed. Awaiting human OWNER review and merge.
- **2026-07-30**: AI Factory (`ada-coder-bot`) has started implementing the identity and refs pattern for `ComputeMachineImage` (Issue #12076).
- **2026-07-29**: Step 1 is already completed and merged. Initiated Step 2 by creating GitHub Issue #12076 and assigning to `daedalus-agent-bot`.
