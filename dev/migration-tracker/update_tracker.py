#!/usr/bin/env python3
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import glob
import json
import os
import re
import subprocess
import sys

# Constants
STATIC_CONFIG_PATH = "pkg/controller/resourceconfig/static_config.go"
DATA_JSON_PATH = "dev/migration-tracker/data.json"
COORDINATOR_ISSUE_NUMBER = "10588"
TRACKING_COMMENT_HEADER = "### Migration Progress Tracker Summary"

def run_command(cmd, check=True):
    print(f"Running command: {' '.join(cmd)}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if check and res.returncode != 0:
        print(f"Error executing command: {' '.join(cmd)}")
        print(f"STDOUT:\n{res.stdout}")
        print(f"STDERR:\n{res.stderr}")
        res.check_returncode()
    return res.stdout

def get_author_login(item):
    if "author" in item and isinstance(item["author"], dict):
        return item["author"].get("login", "")
    return ""

def main():
    if not os.path.exists(DATA_JSON_PATH):
        print(f"Error: {DATA_JSON_PATH} not found.")
        sys.exit(1)
    if not os.path.exists(STATIC_CONFIG_PATH):
        print(f"Error: {STATIC_CONFIG_PATH} not found.")
        sys.exit(1)

    print("Step 1: Identified Coordinator Issue Context.")
    print(f"Coordinator Issue Number: {COORDINATOR_ISSUE_NUMBER}")

    # Load data.json
    with open(DATA_JSON_PATH, "r") as f:
        data = json.load(f)

    kinds = [item["kind"] for item in data]
    sorted_kinds = sorted(kinds, key=len, reverse=True)
    print(f"Loaded {len(kinds)} kinds from data.json.")

    # Step 2: Audit Ground Reality in Code (Source of Truth)
    direct_registered = set()
    entry_pattern = re.compile(r'Group:\s*"([^"]+)",\s*Kind:\s*"([^"]+)"')
    with open(STATIC_CONFIG_PATH, "r") as f:
        for line in f:
            line_clean = line.split("//")[0].strip()
            if not line_clean:
                continue
            m = entry_pattern.search(line_clean)
            if m:
                group_val, kind_val = m.groups()
                group_clean = group_val.replace(".cnrm.cloud.google.com", "")
                if "ReconcilerTypeDirect" in line_clean:
                    direct_registered.add((group_clean, kind_val))
                    direct_registered.add(kind_val)

    print(f"Found {len(direct_registered)} registered direct controllers in static_config.go.")

    # Step 3: Scan GitHub for Active and External Work (SET 1 & SET 2)
    # 1. Active Migration Workflows/Issues (SET 1)
    print("Fetching overseer migration workflow issues...")
    cmd = [
        "gh", "issue", "list", "--state", "all",
        "--label", "overseer,workflow/migrate",
        "--json", "number,title,labels,assignees,createdAt,state,url",
        "--limit", "1000"
    ]
    overseer_issues = json.loads(run_command(cmd))
    print(f"Found {len(overseer_issues)} overseer migration issues.")

    overseer_issues_by_kind = {}
    for issue in overseer_issues:
        title = issue["title"]
        if "TRACKER:" in title:
            continue
        matched_kind = None
        for k in sorted_kinds:
            pattern = r'\b' + re.escape(k) + r'\b'
            if re.search(pattern, title, re.IGNORECASE):
                matched_kind = k
                break
        if matched_kind:
            # If we already have an issue for this kind, prefer OPEN over CLOSED, or newer
            if matched_kind not in overseer_issues_by_kind:
                overseer_issues_by_kind[matched_kind] = issue
            else:
                existing = overseer_issues_by_kind[matched_kind]
                if existing["state"].upper() != "OPEN" and issue["state"].upper() == "OPEN":
                    overseer_issues_by_kind[matched_kind] = issue
                elif existing["state"].upper() == issue["state"].upper() and issue["createdAt"] > existing["createdAt"]:
                    overseer_issues_by_kind[matched_kind] = issue

    overseer_issue_numbers = {iss["number"] for iss in overseer_issues}

    # 2. Search for Other/External Issues and PRs (SET 2)
    print("Fetching open issues and PRs for external work matching...")
    open_issues = json.loads(run_command([
        "gh", "issue", "list", "--state", "open", "--limit", "5000",
        "--json", "number,title,url,author,state"
    ]))
    open_prs = json.loads(run_command([
        "gh", "pr", "list", "--state", "open", "--limit", "5000",
        "--json", "number,title,url,author,state"
    ]))

    external_works_by_kind = {}
    for item in open_issues + open_prs:
        author = get_author_login(item).lower()
        if "bot" in author or "robot" in author:
            continue
        if item["number"] in overseer_issue_numbers:
            continue
        title = item.get("title", "")
        for k in sorted_kinds:
            pattern = r'\b' + re.escape(k) + r'\b'
            if re.search(pattern, title, re.IGNORECASE):
                external_works_by_kind.setdefault(k, set()).add(item["number"])

    print(f"Mapped external work for {len(external_works_by_kind)} kinds.")

    # Helper function to determine stage, steps, and identity/ref presence
    def determine_stage_and_steps(service, kind, version):
        service_lower = service.lower()
        kind_lower = kind.lower()
        suffix = kind_lower
        if kind_lower.startswith(service_lower) and len(kind_lower) > len(service_lower):
            suffix = kind_lower[len(service_lower):]

        # Stage 5 (Controller Implemented)
        stage5_patterns = [
            f"pkg/controller/direct/{service_lower}/{kind_lower}_controller.go",
            f"pkg/controller/direct/{service_lower}/{suffix}_controller.go",
            f"pkg/controller/direct/{service_lower}/{kind}_controller.go",
            f"pkg/controller/direct/{service_lower}/adapter.go",
            f"pkg/controller/direct/{kind_lower}/adapter.go",
            f"pkg/controller/direct/{kind_lower}/{kind_lower}_controller.go",
        ]
        is_stage5 = any(os.path.exists(f) for f in stage5_patterns)

        # Stage 4 (MockGCP / E2E Fixtures)
        is_stage4 = False
        if os.path.exists(f"mockgcp/mock{service_lower}") or os.path.exists(f"mockgcp/mock{kind_lower}"):
            is_stage4 = True
        if os.path.exists(f"pkg/controller/direct/{service_lower}"):
            for f in os.listdir(f"pkg/controller/direct/{service_lower}"):
                if "test" in f.lower() or "fixture" in f.lower():
                    is_stage4 = True
                    break
        basic_dir = f"pkg/test/resourcefixture/testdata/basic/{service_lower}"
        if os.path.exists(basic_dir):
            for root, dirs, files in os.walk(basic_dir):
                for d in dirs:
                    if d.lower() in (kind_lower, suffix):
                        is_stage4 = True
                        break

        # Stage 3 (KRM Fuzzer)
        stage3_patterns = [
            f"pkg/controller/direct/{service_lower}/{kind_lower}_fuzzer.go",
            f"pkg/controller/direct/{service_lower}/{suffix}_fuzzer.go",
            f"pkg/controller/direct/{service_lower}/{kind}_fuzzer.go",
            f"pkg/controller/direct/{kind_lower}/{kind_lower}_fuzzer.go",
        ]
        is_stage3 = any(os.path.exists(f) for f in stage3_patterns)

        # Check identity & reference files across all versions
        identities = glob.glob(f"apis/{service_lower}/*/{kind_lower}_identity.go") + \
                     glob.glob(f"apis/{service_lower}/*/{suffix}_identity.go") + \
                     glob.glob(f"apis/{kind_lower}/*/{kind_lower}_identity.go")
        references = glob.glob(f"apis/{service_lower}/*/{kind_lower}_reference.go") + \
                     glob.glob(f"apis/{service_lower}/*/{suffix}_reference.go") + \
                     glob.glob(f"apis/{kind_lower}/*/{kind_lower}_reference.go")

        has_identity = bool(identities)
        has_reference = bool(references)
        has_both_id_ref = has_identity and has_reference
        is_stage2 = has_identity or has_reference

        # Stage 1 (Direct KRM Types)
        types = glob.glob(f"apis/{service_lower}/*/{kind_lower}_types.go") + \
                glob.glob(f"apis/{service_lower}/*/{suffix}_types.go") + \
                glob.glob(f"apis/{service_lower}/*/{kind}_types.go") + \
                glob.glob(f"apis/{kind_lower}/*/{kind_lower}_types.go")
        is_stage1 = bool(types)

        stage = "Investigation/Setup"
        if is_stage5:
            stage = "Stage 5 (Controller Implemented)"
            steps = {
                "gen-types": True,
                "identity-reference": has_both_id_ref,
                "mapper-fuzzer": is_stage3,
                "mocks": is_stage4,
                "controller": True,
                "tests": True
            }
        elif is_stage4:
            stage = "Stage 4 (MockGCP/E2E Fixtures)"
            steps = {
                "gen-types": True,
                "identity-reference": has_both_id_ref,
                "mapper-fuzzer": is_stage3,
                "mocks": True,
                "controller": False,
                "tests": True
            }
        elif is_stage3:
            stage = "Stage 3 (KRM Fuzzer)"
            steps = {
                "gen-types": True,
                "identity-reference": has_both_id_ref,
                "mapper-fuzzer": True,
                "mocks": is_stage4,
                "controller": False,
                "tests": False
            }
        elif is_stage2:
            stage = "Stage 2 (Identity & Reference Types)"
            steps = {
                "gen-types": True,
                "identity-reference": has_both_id_ref,
                "mapper-fuzzer": False,
                "mocks": is_stage4,
                "controller": False,
                "tests": False
            }
        elif is_stage1:
            stage = "Stage 1 (Direct KRM Types)"
            steps = {
                "gen-types": True,
                "identity-reference": False,
                "mapper-fuzzer": False,
                "mocks": is_stage4,
                "controller": False,
                "tests": False
            }
        else:
            steps = {
                "gen-types": False,
                "identity-reference": False,
                "mapper-fuzzer": False,
                "mocks": os.path.exists(f"mockgcp/mock{service_lower}"),
                "controller": False,
                "tests": False
            }

        return stage, steps, has_both_id_ref

    # Helper function to generate notes
    def generate_notes(existing_notes, is_missing_ref_id, closed_tracking_issue_anomaly=None, external_works=None):
        notes_list = []
        if is_missing_ref_id:
            notes_list.append("Missing _reference.go or _identity.go")
        if closed_tracking_issue_anomaly:
            notes_list.append(closed_tracking_issue_anomaly)
        if existing_notes:
            for note in existing_notes.split(','):
                note = note.strip()
                if not note:
                    continue
                if "closed but direct controller is not registered" in note:
                    continue
                if "Missing _reference.go or _identity.go" in note:
                    continue
                if "External Work:" in note:
                    continue
                if "Community PR:" in note:
                    continue
                notes_list.append(note)
        if external_works:
            for ew in sorted(list(external_works)):
                notes_list.append(f"External Work: #{ew}")
        return ", ".join(notes_list)

    # Process each resource in data.json
    for item in data:
        gp = item["group"]
        kd = item["kind"]
        version = item["version"]
        is_direct = (gp, kd) in direct_registered or kd in direct_registered

        stage, steps, has_both_id_ref = determine_stage_and_steps(gp, kd, version)
        ext_works = external_works_by_kind.get(kd, None)
        overseer_issue = overseer_issues_by_kind.get(kd, None)

        is_missing_ref_id = False
        if stage != "Investigation/Setup" and not has_both_id_ref:
            is_missing_ref_id = True

        if is_direct:
            # Step 2: Direct controller is registered
            item["state"] = "Completed"
            item["stage"] = "Stage 5 (Controller Implemented)"
            item["trackingIssue"] = ""
            item["assignee"] = ""
            item["notes"] = ""
            item["steps"] = {
                "gen-types": True,
                "identity-reference": True,
                "mapper-fuzzer": True,
                "mocks": True,
                "controller": True,
                "tests": True
            }
            if "Direct" not in item.get("supportedControllers", []):
                item.setdefault("supportedControllers", []).append("Direct")
        else:
            # Step 2: Direct controller is NOT registered
            if item.get("state") == "Completed":
                print(f"Reverting {kd} from Completed")
                item["state"] = "In Progress"

            closed_tracking_issue_anomaly = None
            if overseer_issue:
                if overseer_issue["state"].upper() == "OPEN":
                    item["state"] = "In Progress"
                    item["trackingIssue"] = f"[#{overseer_issue['number']}]({overseer_issue['url']})"
                    item["assignee"] = ", ".join(a["login"] for a in overseer_issue.get("assignees", []))
                else:  # CLOSED
                    item["trackingIssue"] = "N/A"
                    item["assignee"] = ""
                    closed_tracking_issue_anomaly = f"Tracking issue #{overseer_issue['number']} is closed but direct controller is not registered in code"
                    if stage != "Investigation/Setup" or ext_works:
                        item["state"] = "In Progress"
                    else:
                        item["state"] = "Not Started"
            else:
                item["trackingIssue"] = "N/A"
                item["assignee"] = ""
                if stage != "Investigation/Setup" or ext_works:
                    item["state"] = "In Progress"
                else:
                    item["state"] = "Not Started"

            item["stage"] = stage
            item["steps"] = steps
            item["notes"] = generate_notes(item.get("notes", ""), is_missing_ref_id, closed_tracking_issue_anomaly, ext_works)

    # Step 5: Identify Next Pending Resources
    completed_kinds = {item["kind"] for item in data if item["state"] == "Completed"}
    pending_candidates = []
    for item in data:
        if item["state"] == "Not Started" and item["defaultController"] in ("Terraform", "DCL"):
            deps = item.get("dependencies", [])
            all_deps_completed = True
            for dep in deps:
                dep_in_data = any(x["kind"] == dep for x in data)
                if dep_in_data and dep not in completed_kinds:
                    all_deps_completed = False
                    break
            if all_deps_completed:
                pending_candidates.append(item)

    pending_candidates.sort(key=lambda x: x["sortOrder"])

    # Step 6: Save local tracking data to dev/migration-tracker/data.json
    with open(DATA_JSON_PATH, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved {DATA_JSON_PATH}")

    # Step 7: Update Summary Comment on Coordinator Issue
    completed_count = sum(1 for item in data if item["state"] == "Completed")
    in_progress_count = sum(1 for item in data if item["state"] == "In Progress")
    pending_count = sum(1 for item in data if item["state"] == "Not Started")
    total_count = len(data)

    print(f"Summary counts: Completed={completed_count}, In Progress={in_progress_count}, Pending={pending_count}, Total={total_count}")

    # Format Markdown summary
    summary_lines = []
    summary_lines.append(f"{TRACKING_COMMENT_HEADER}\n")
    summary_lines.append("## High-Level Status")
    summary_lines.append("| State | Count |")
    summary_lines.append("|-------|-------|")
    summary_lines.append(f"| Completed | {completed_count} |")
    summary_lines.append(f"| In Progress | {in_progress_count} |")
    summary_lines.append(f"| Pending | {pending_count} |")
    summary_lines.append(f"| Total | {total_count} |\n")

    summary_lines.append("## In Progress Resources")
    summary_lines.append("| Kind | Current Stage | Tracking Issue/PR | Assignee | Notes |")
    summary_lines.append("|------|---------------|-------------------|----------|-------|")
    in_progress_items = sorted([item for item in data if item["state"] == "In Progress"], key=lambda x: x["kind"])
    for item in in_progress_items:
        assignee_str = item.get("assignee", "")
        summary_lines.append(f"| {item['kind']} | {item['stage']} | {item['trackingIssue']} | {assignee_str} | {item['notes']} |")

    summary_lines.append("\n## Next Resources (Pending & Unblocked)")
    summary_lines.append("| Kind | Sort Order | Default Controller | Dependencies | Notes |")
    summary_lines.append("|------|------------|--------------------|--------------|-------|")
    for item in pending_candidates:
        deps_str = ", ".join(item.get("dependencies", []))
        summary_lines.append(f"| {item['kind']} | {item['sortOrder']} | {item['defaultController']} | {deps_str} | {item['notes']} |")

    summary_lines.append("\n## Completed Resources")
    summary_lines.append("| Kind | Default Controller | Date Completed / Notes |")
    summary_lines.append("|------|--------------------|------------------------|")
    completed_items = sorted([item for item in data if item["state"] == "Completed"], key=lambda x: x["kind"])
    for item in completed_items:
        summary_lines.append(f"| {item['kind']} | {item['defaultController']} | Registered in code |")

    summary_body = "\n".join(summary_lines) + "\n"

    # Write summary body to file
    with open("summary_comment.md", "w") as f:
        f.write(summary_body)

    # Find existing tracker comment on coordinator issue
    comments_res = json.loads(run_command(["gh", "issue", "view", COORDINATOR_ISSUE_NUMBER, "--json", "comments"]))
    comments_list = comments_res.get("comments", [])

    comment_db_id = None
    for comment in reversed(comments_list):
        if TRACKING_COMMENT_HEADER in comment.get("body", ""):
            comment_url = comment.get("url", "")
            m = re.search(r"issuecomment-(\d+)", comment_url)
            if m:
                comment_db_id = m.group(1)
                break

    if comment_db_id:
        print(f"Updating existing comment ID: {comment_db_id}...")
        run_command([
            "gh", "api", "--method", "PATCH",
            f"repos/:owner/:repo/issues/comments/{comment_db_id}",
            "-F", "body=@summary_comment.md"
        ])
        print("Successfully updated coordinator issue comment.")
    else:
        print("Creating new tracker comment...")
        run_command([
            "gh", "issue", "comment", COORDINATOR_ISSUE_NUMBER,
            "-F", "body=@summary_comment.md"
        ])
        print("Successfully created coordinator issue comment.")

if __name__ == "__main__":
    main()
