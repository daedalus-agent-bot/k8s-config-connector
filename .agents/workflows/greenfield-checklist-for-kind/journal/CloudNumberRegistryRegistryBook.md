# Migration Journal: CloudNumberRegistryRegistryBook

**Current Step:** Step 2: Direct Controller, E2E fixtures and Fuzzer

## Progress Tracking

| Step | Name | Issue | PR | Status | Date Started | Date Completed |
|------|------|-------|----|--------|--------------|----------------|
| 1 | Direct KRM Types & Identity | [#12852](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12852) | [#12864](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12864) | Merged | 2026-09-09 | 2026-09-10 |
| 2 | Direct Controller & E2E | [#12890](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12890) | [#12895](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12895) | PR Created | 2026-09-10 | - |
| 3 | mockGCP Generation | - | - | Pending | - | - |
| 4 | mockGCP RealGCP Alignment | - | - | Pending | - | - |

## Status Updates

- **2026-09-11**: Verified that all CI checks (including E2E fixture tests, unit tests, and linters) have successfully passed on Pull Request [#12895](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12895). The PR is fully green and now awaiting human OWNER review and approval to be merged.
- **2026-09-11**: Pull Request [#12895](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12895) has been created. It is currently undergoing automated validation and CI check resolution.
- **2026-09-10**: Child issue [#12890](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12890) is currently being worked on by the AI Factory. Awaiting Pull Request creation.
- **2026-09-10**: Step 1 (Direct KRM Types & Identity) has been successfully merged. Transitioning to Step 2: Direct Controller, E2E fixtures and Fuzzer. Created child issue [#12890](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12890).
- **2026-09-10**: Pull Request [#12864](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12864) has been officially approved by reviewer `anhdle-sso`. It is currently awaiting final merge by a human OWNER before we can transition to Step 2.
- **2026-09-10**: Verified that all CI checks have fully passed for Pull Request [#12864](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12864). The PR is fully green and now awaiting human review, approval, and merging by the human OWNER.
- **2026-09-10**: Pull Request [#12864](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12864) has successfully resolved all auto-reviewer feedback (including refactoring `.spec.claimedScopes` to `.spec.claimedScopeRefs` as a slice of project references). The PR has passed all CI presubmits, has been fully approved by the auto-reviewer, and is now awaiting human OWNER review and merging.
- **2026-09-10**: Pull Request [#12864](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12864) has successfully passed all CI presubmits and the `Location` field issue flagged by the auto-reviewer has been resolved (changed to a pointer `*string`). The PR is fully green and now awaiting human review/approval and merging.
- **2026-09-10**: Pull Request [#12864](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12864) remains open. CI checks show failures in `unit-tests-1-of-4` and `presubmit-gatekeeper`, which are being investigated.
- **2026-09-09**: Pull Request [#12864](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12864) was created for Step 1 (KRM Types & Identity). It is currently open, with some CI check failures being investigated by the automated factory watcher.
- **2026-09-09**: Initiated Greenfield Migration for `CloudNumberRegistryRegistryBook`. Created child issue [#12852](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12852) for Step 1.
