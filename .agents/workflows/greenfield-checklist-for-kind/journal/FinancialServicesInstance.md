# Greenfield Migration Journal: FinancialServicesInstance

This journal tracks the progress of migrating `FinancialServicesInstance` to a direct KRM controller.

**Current Step:** Step 3: MockGCP Implementation

## Progress Table

| Step | Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
|------|------|--------------|---------------------|--------|--------------|----------------|
| 1 | Direct API Types & Identity | [#10268](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10268) | [#13642](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/13642) | Completed | 2026-06-17 | 2026-10-02 |
| 2 | Direct Controller & E2E Fixtures | [#13673](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/13673) | [#13676](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/13676) | Completed | 2026-10-02 | 2026-10-08 |
| 3 | MockGCP Implementation | [#13837](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/13837) | - | Open | 2026-10-08 | - |
| 4 | MockGCP Alignment | - | - | Not Started | - | - |

## Status Update Notes
*   **2026-10-08**: Step 2 completed (PR #13676 merged). Step 3 initialized: Issue #13837 created for MockGCP implementation.
*   **2026-10-02**: Overseer checked progress. PR #13676 created for Step 2 (Issue #13673). CI check `validate-ensure` failed. Waiting for PR to pass CI and merge.
*   **2026-10-02**: Step 1 completed (PR #13642 merged). Step 2 initialized: Issue #13673 created for Direct Controller, E2E fixtures, and Fuzzer.
*   **2026-10-02**: Overseer checked progress. Previous PR #10343 was closed and replaced by PR #13642. PR #13642 is currently OPEN. Waiting for PR to pass CI and merge.
*   **2026-09-19**: Overseer checked progress. PR #10343 is currently OPEN. CI check `tests-e2e-fixtures` is failing. Waiting for PR to pass CI and merge.
*   **2026-06-17**: Initialized Step 1. Issue #10268 was opened and PR #10343 was created.
