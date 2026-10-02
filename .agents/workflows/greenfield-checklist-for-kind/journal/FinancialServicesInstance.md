# Greenfield Migration Journal: FinancialServicesInstance

This journal tracks the progress of migrating `FinancialServicesInstance` to a direct KRM controller.

**Current Step:** Step 1: Direct API Types and Identity and Reference Types Pattern

## Progress Table

| Step | Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
|------|------|--------------|---------------------|--------|--------------|----------------|
| 1 | Direct API Types & Identity | [#10268](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10268) | [#13642](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/13642) | PR Created | 2026-06-17 | - |
| 2 | Direct Controller & E2E Fixtures | - | - | Not Started | - | - |
| 3 | MockGCP Implementation | - | - | Not Started | - | - |
| 4 | MockGCP Alignment | - | - | Not Started | - | - |

## Status Update Notes
*   **2026-10-02**: Overseer checked progress. Previous PR #10343 was closed and replaced by PR #13642. PR #13642 is currently OPEN. Waiting for PR to pass CI and merge.
*   **2026-09-19**: Overseer checked progress. PR #10343 is currently OPEN. CI check `tests-e2e-fixtures` is failing. Waiting for PR to pass CI and merge.
*   **2026-06-17**: Initialized Step 1. Issue #10268 was opened and PR #10343 was created.
