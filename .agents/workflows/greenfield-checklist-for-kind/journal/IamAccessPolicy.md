# Greenfield Migration Journal: IamAccessPolicy

## Current Step
Step 1: Direct API Types and Identity

## Migration Progress Tracking

| Step | Task Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Direct API Types and Identity | [Issue #10278](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10278) | [PR #10989](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10989) | PR Created (CI Failing) | 2026-06-29 | - |
| 2 | Direct Controller and E2E | - | - | Pending | - | - |
| 3 | MockGCP Generation | - | - | Pending | - | - |
| 4 | MockGCP Alignment | - | - | Pending | - | - |

## Status Log
* **2026-06-30**: Monitored PR #10989 and verified CI checks are still failing (`unit-tests`, `validate-generated-files`, and `validations`). Confirmed PR is currently assigned to `hopper-coder-bot` and awaiting updates.
* **2026-06-30**: Identified open PR #10989 by hopper-coder-bot for Step 1. CI checks failed (specifically `validate-generated-files` and `validations`). Assigned the PR back to `hopper-coder-bot` for troubleshooting and fixes.
* **2026-06-30**: Verified status of Step 1. Issue #10278 is open, but no active PR has been opened yet. Waiting for coder bots to start a new PR.
* **2026-06-29**: Greenfield migration tracking initialized. Checked existing issues and found that Step 1 issue #10278 is already open but currently has no active PR (previous PR #10321 was closed without merging).
