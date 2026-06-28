# Migration Journal: OSConfigGuestPolicy

Current Step: Step 1: Direct API Types

| Step | Step Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
|---|---|---|---|---|---|---|
| 1 | Direct API Types | [#10940](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10940) | [#10943](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10943) | PR Passing / Awaiting Merge | 2026-06-28 | |
| 2 | Identity and Reference Types Pattern | | | Not Started | | |
| 3 | Create a Round-Trip KRM Fuzzer | | | Not Started | | |
| 4 | Ensure MockGCP matches real gcp behavior | | | Not Started | | |
| 5 | Implement Direct Controller & E2E Fixtures | | | Not Started | | |

## History / Status Updates

- **2026-06-28**: Checked status of PR [#10943](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10943). All CI checks are fully passing, and the PR is open and awaiting review/merge by owner `barney-s`.
- **2026-06-28**: All 193 CI check-runs passed successfully. Assigned the PR [#10943](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10943) to owner `barney-s` for review, approval, and merge.
- **2026-06-28**: Verified PR [#10943](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10943) is still open. CI checks `unit-tests` and `validate-generated-files` are currently failing. The PR is assigned to `lovelace-coder-bot`, and `argus-watcher-bot` is currently investigating the failures.
- **2026-06-28**: Analyzed CI check failures for PR [#10943](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10943). `validate-generated-files` failed because documentation file `scripts/generate-google3-docs/resource-reference/generated/resource-docs/osconfig/osconfigguestpolicy.md` is out-of-date (needs `make resource-docs`). `unit-tests` failed because `TestMissingRefs` found an unexpected diff for `osconfigguestpolicies` in `testdata/exceptions/missingrefs.txt` (needs to run presubmit script to update exceptions). `argus-watcher-bot` is currently investigating.
- **2026-06-28**: Pull Request [#10943](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10943) has failed CI check runs (specifically `unit-tests` and `validate-generated-files`). Re-assigned the PR to author bot `lovelace-coder-bot` to investigate and apply fixes.
- **2026-06-28**: Pull Request [#10943](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10943) has been created by `lovelace-coder-bot` to resolve issue #10940. CI checks are currently in progress.
- **2026-06-28**: Verified that issue #10940 is still open and assigned to `lovelace-coder-bot`. No Pull Request has been created yet, and the sandbox run is still in progress.
- **2026-06-28**: Checked status of Step 1 on issue #10940. No Pull Request has been created yet. The sandbox run by `lovelace-coder-bot` is still in progress.
- **2026-06-28**: Checked status of Step 1 issue #10940. Assigned to lovelace-coder-bot; AI Factory started sandbox run.
- **2026-06-28**: Created parent tracker and initialized Step 1 issue #10940 to implement direct KRM types and generate.sh for OSConfigGuestPolicy.
