# Greenfield Migration Journal: AIPlatformOnlineEvaluator

Current Step: Step 2 - Direct Controller, E2E fixtures and Fuzzer

## Progress Tracking

| Step | Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Direct KRM types, identity, generate.sh | [#12834](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12834) | [#12861](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12861) | Merged | 2026-09-09 | 2026-11-04 |
| 2 | Direct controller, E2E, fuzzer | [#14933](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14933) | [#14948](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14948) | PR Created | 2026-11-05 | - |
| 3 | MockGCP and Alignment | - | - | Pending | - | - |
| 4 | Align MockGCP logs with RealGCP | - | - | Pending | - | - |

## Log / History
- **2026-09-09**: Initialized the greenfield migration checklist and journal for `AIPlatformOnlineEvaluator`. Created Step 1 GitHub issue [#12834](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12834).
- **2026-09-09**: Pull Request [#12861](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12861) was created for Step 1. Currently investigating CI check failures.
- **2026-09-10**: PR [#12861](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12861) successfully resolved the initial failures and passed all CI checks. It is currently undergoing automated review; `reviewbot-robot` requested changes to address a GVK mapping mismatch in `DialogflowCXAgentRef` and a generation rule omission. `argus-watcher-bot` is currently addressing the feedback. The workflow remains in Step 1.
- **2026-09-10**: PR [#12861](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12861) has successfully resolved all review feedback and passed all automated checks. It has been marked with `overseer/ready-for-human` and is awaiting review and merge by human maintainers.
- **2026-11-04**: PR [#12861](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12861) has been merged to master. Step 1 completed.
- **2026-11-05**: Step 1b skipped (legacy Step 1 finalized types on master without open judgement entries). Opened Step 2 GitHub issue [#14933](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14933) to implement direct controller, E2E fixtures, and fuzzer.
- **2026-11-05**: Pull Request [#14948](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14948) was created for Step 2.
