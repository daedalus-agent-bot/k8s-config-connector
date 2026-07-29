# Greenfield Migration Journal: VertexAIExtension

**Current Step**: Step 1: Direct KRM Types and Identity

## Migration Progress

| Step | Step Name | GitHub Issue | GitHub PR | Status | Date Started | Date Completed |
|------|-----------|--------------|-----------|--------|--------------|----------------|
| 1 | Direct KRM Types & Identity | [#12027](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12027) | [#12036](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12036) | PR Created | 2026-07-29 | - |
| 2 | Direct Controller & E2E | - | - | Pending | - | - |
| 3 | mockGCP Generation | - | - | Pending | - | - |
| 4 | MockGCP Alignment | - | - | Pending | - | - |

## Status Update Notes
* **2026-07-29**: Verified PR [#12036](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12036) status: all 150+ CI checks are successfully passing (green) and no failures are returned. The PR is still open, pending review and merge by human owners.
* **2026-07-29**: Monitored Step 1 PR [#12036](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12036). All 150+ CI checks are fully green and successful. The PR remains open, awaiting human OWNER review, approval, and merge before we can proceed to Step 2.
* **2026-07-29**: Checked pull request status. Verified all CI checks are green and passing. The PR remains open, awaiting human OWNER review and merge before proceeding to Step 2.
* **2026-07-29**: Monitoring progress. Verified all 150+ CI check-runs have completed successfully. PR [#12036](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12036) remains open, waiting for human OWNER review and merge to complete Step 1.
* **2026-07-29**: Performed verification check on PR [#12036](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12036). All 150+ CI checks continue to pass successfully in a green state. Awaiting human OWNER review, approval, and merge to proceed to Step 2.
* **2026-07-29**: Monitoring progress. Confirmed PR [#12036](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12036) remains open and all 150+ CI checks continue to pass successfully in a clean green state, awaiting human OWNER review and merge.
* **2026-07-29**: Checked pull request status. Step 1 PR [#12036](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12036) remains open and fully verified green. All CI checks are passing successfully. Waiting for human OWNER merge.
* **2026-07-29**: Verified PR [#12036](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12036) status: all 150+ CI checks are successfully passing (green). The PR is still open, pending review and merge by human owners.
* **2026-07-29**: Monitoring progress. Confirmed PR [#12036](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12036) is still open and all CI checks are in a fully successful green state. Awaiting human OWNER review, approval, and merge to proceed to Step 2.
* **2026-07-29**: Performed check. Confirmed all 150+ CI check-runs are completely successful. PR [#12036](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12036) is in a clean green state and awaiting human review, approval, and merge.
* **2026-07-29**: Performed periodic check. PR [#12036](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12036) remains open and all CI check-runs continue to pass successfully. It is currently awaiting human review, approval, and merge.
* **2026-07-29**: Verified that all core CI check-runs (including `unit-tests`, `validate-generated-files`, and `validations`) have passed successfully on PR [#12036](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12036). The PR is now ready and waiting for human review and approval to merge.
* **2026-07-29**: Analyzed `unit-tests` failure on PR [#12036](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12036) and identified failing api-checks: `TestCRDFieldPresenceInTestsForAlpha`, `TestSpecShouldNotContainEtag`, and `TestMissingRefs`. Assigned PR #12036 back to `neumann-coder-bot` to add the necessary exception listings under `tests/apichecks/testdata/exceptions/`.
* **2026-07-29**: Identified `unit-tests` failure (`TestMissingRefs`) on PR [#12036](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12036), where several spec fields under `vertexaiextensions` were flagged as missing references. Assigned PR back to `neumann-coder-bot` to resolve the test failure.
* **2026-07-29**: Analyzed CI failures on PR [#12036](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12036) and identified OpenAPI schema validation issues due to the recursive `Schema` type in `types.generated.go`. AI Factory has automatically started investigation.
* **2026-07-29**: Step 1 PR [#12036](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12036) created by neumann-coder-bot. Assigned the PR to neumann-coder-bot to investigate failing checks.
* **2026-07-29**: Started Greenfield migration for VertexAIExtension. Created Step 1 GitHub issue [#12027](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12027) to coordinate implementing direct KRM types, identity, and generation.
