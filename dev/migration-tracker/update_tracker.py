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

import os
import re
import sys
import json
import subprocess

# Service group exceptions mapping for mockgcp matching
group_to_mock = {
    "vertexai": "aiplatform",
    "workflowexecutions": "workflowexecution",
}

def load_data(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

def save_data(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

def merge_notes_helper(original_notes, missing_files, closed_anomaly, external_works):
    parts = []
    if original_notes:
        for part in original_notes.split(","):
            part_strip = part.strip()
            if not part_strip:
                continue
            if "Missing _reference.go" in part_strip:
                continue
            if "Tracking issue" in part_strip and "is closed" in part_strip:
                continue
            if "External Work:" in part_strip:
                continue
            parts.append(part_strip)
    
    if missing_files:
        parts.append("Missing _reference.go or _identity.go")
    if closed_anomaly:
        parts.append(closed_anomaly)
    if external_works:
        unique_works = []
        for ew in external_works:
            if ew not in unique_works:
                unique_works.append(ew)
        parts.extend(unique_works)
        
    return ", ".join(parts)

def main():
    tracker_filepath = "dev/migration-tracker/data.json"
    static_config_path = "pkg/controller/resourceconfig/static_config.go"
    issue_number = "10588"

    if not os.path.exists(tracker_filepath):
        print(f"Error: tracking data file not found at {tracker_filepath}")
        sys.exit(1)

    print("Loading migration tracker data...")
    data = load_data(tracker_filepath)
    kinds_in_tracker = {item["kind"]: item for item in data}

    # Step 2: Audit Ground Reality in Code (Source of Truth)
    print("Parsing static_config.go for registered direct controllers...")
    if not os.path.exists(static_config_path):
        print(f"Error: {static_config_path} not found")
        sys.exit(1)

    with open(static_config_path, "r") as f:
        static_config_content = f.read()

    # Find the ControllerConfigStatic block
    map_block_match = re.search(r"var ControllerConfigStatic = ResourcesControllerMap\{(.*?)\n\}", static_config_content, re.DOTALL)
    if not map_block_match:
        print("Error: Could not parse ControllerConfigStatic in static_config.go")
        sys.exit(1)

    map_content = map_block_match.group(1)
    registered_kinds = set()
    for line in map_content.splitlines():
        line = line.strip()
        if not line or line.startswith("//"):
            continue
        kind_match = re.search(r'Kind:\s*"([^"]+)"', line)
        if kind_match:
            kind = kind_match.group(1)
            # Check if ReconcilerTypeDirect is supported for this resource
            parts = line.split(":", 1)
            if len(parts) == 2:
                config_part = parts[1]
                sc_match = re.search(r"SupportedControllers:\s*\[\]k8s\.ReconcilerType\s*\{(.*?)\}", config_part)
                if sc_match:
                    sc_content = sc_match.group(1)
                    if "k8s.ReconcilerTypeDirect" in sc_content:
                        registered_kinds.add(kind)

    print(f"Found {len(registered_kinds)} registered direct controller kinds in static_config.go")

    # Step 3: Scan GitHub for Active and External Work (SET 1 & SET 2)
    print("Fetching overseer/workflow migration issues from GitHub...")
    issues_cmd = [
        "gh", "issue", "list",
        "--state", "all",
        "--label", "overseer,workflow/migrate",
        "--limit", "1000",
        "--json", "number,title,labels,assignees,createdAt,state,url"
    ]
    issues_data = json.loads(subprocess.check_output(issues_cmd).decode("utf-8"))
    print(f"Retrieved {len(issues_data)} migration workflow issues.")

    print("Fetching all open issues in bulk...")
    open_issues_cmd = [
        "gh", "issue", "list",
        "--state", "open",
        "--limit", "1000",
        "--json", "number,title,url,assignees,author,state"
    ]
    open_issues_data = json.loads(subprocess.check_output(open_issues_cmd).decode("utf-8"))
    print(f"Retrieved {len(open_issues_data)} open issues.")

    print("Fetching all open PRs in bulk...")
    open_prs_cmd = [
        "gh", "pr", "list",
        "--state", "open",
        "--limit", "1000",
        "--json", "number,title,url,author,state"
    ]
    open_prs_data = json.loads(subprocess.check_output(open_prs_cmd).decode("utf-8"))
    print(f"Retrieved {len(open_prs_data)} open PRs.")

    # Walk codebase directories once to build lookup structures for lightning-fast stage checking
    print("Analyzing filesystem directory structures...")
    apis_files = []
    for root, dirs, files in os.walk("apis"):
        for file in files:
            apis_files.append(os.path.join(root, file).replace("\\", "/"))

    direct_files = []
    for root, dirs, files in os.walk("pkg/controller/direct"):
        for file in files:
            direct_files.append(os.path.join(root, file).replace("\\", "/"))

    mockgcp_dirs = []
    if os.path.exists("mockgcp"):
        for name in os.listdir("mockgcp"):
            if os.path.isdir(os.path.join("mockgcp", name)):
                mockgcp_dirs.append(name.lower())

    basic_test_dirs = []
    for root, dirs, files in os.walk("pkg/test/resourcefixture/testdata/basic"):
        for d in dirs:
            basic_test_dirs.append(d.lower())

    # Helper stage-checking functions
    def check_stage5(group, kind_lower):
        target_ctrl = f"pkg/controller/direct/{group}/{kind_lower}_controller.go".lower()
        target_adapter = f"pkg/controller/direct/{group}/adapter.go".lower()
        for f in direct_files:
            f_lower = f.lower()
            if f_lower == target_ctrl or f_lower == target_adapter:
                return True
            if f_lower.endswith(f"/{kind_lower}_controller.go") and f_lower.startswith(f"pkg/controller/direct/{group}/"):
                return True
        return False

    def check_stage4(group, kind_lower):
        mock_name = group_to_mock.get(group, group)
        if f"mock{mock_name}" in mockgcp_dirs:
            return True
        if kind_lower in basic_test_dirs:
            return True
        for f in direct_files:
            f_lower = f.lower()
            if f_lower.startswith(f"pkg/controller/direct/{group}/") and kind_lower in os.path.basename(f_lower) and "_test.go" in f_lower:
                return True
        return False

    def check_stage3(group, kind_lower):
        target_fuzzer = f"pkg/controller/direct/{group}/{kind_lower}_fuzzer.go".lower()
        for f in direct_files:
            f_lower = f.lower()
            if f_lower == target_fuzzer:
                return True
            if f_lower.endswith(f"/{kind_lower}_fuzzer.go") and f_lower.startswith(f"pkg/controller/direct/{group}/"):
                return True
        return False

    def check_stage2(group, kind_lower):
        for f in apis_files:
            f_lower = f.lower()
            if f_lower.startswith(f"apis/{group}/") and (f_lower.endswith(f"/{kind_lower}_identity.go") or f_lower.endswith(f"/{kind_lower}_reference.go")):
                return True
        return False

    def check_stage1(group, kind_lower):
        for f in apis_files:
            f_lower = f.lower()
            if f_lower.startswith(f"apis/{group}/") and f_lower.endswith(f"/{kind_lower}_types.go"):
                return True
        return False

    def check_any_work_detected(group, kind_lower, has_active_issue):
        if check_stage1(group, kind_lower) or check_stage2(group, kind_lower) or check_stage3(group, kind_lower) or check_stage4(group, kind_lower) or check_stage5(group, kind_lower):
            return True
        return has_active_issue

    def is_bot_or_tracked(author_login, item_url, kind, tracking_issue_url):
        login_lower = author_login.lower()
        if "bot" in login_lower or "robot" in login_lower:
            return True
        if item_url == tracking_issue_url:
            return True
        return False

    # Extract all migration active tasks (SET 1)
    open_migration_issues_by_kind = {}
    closed_migration_issues_by_kind = {}
    for issue in issues_data:
        # Match Kind in title (e.g., "Migrate ComputeNetworkEndpointGroup to Direct controller")
        title = issue["title"]
        kind_match = re.search(r"Migrat(?:e|ing)\s+(\w+)\s+to\s+Direct", title, re.IGNORECASE)
        if kind_match:
            kind = kind_match.group(1)
            if kind in kinds_in_tracker:
                if issue["state"] == "OPEN":
                    open_migration_issues_by_kind[kind] = issue
                elif issue["state"] == "CLOSED":
                    closed_migration_issues_by_kind[kind] = issue

    # Pre-map all external work by Kind (SET 2)
    external_works_by_kind = {}
    for issue in open_issues_data:
        author = issue.get("author", {}).get("login", "") if issue.get("author") else ""
        num = issue["number"]
        url = issue["url"]
        for kind, item in kinds_in_tracker.items():
            if kind in issue["title"] and not is_bot_or_tracked(author, url, kind, item.get("trackingIssue", "")):
                external_works_by_kind.setdefault(kind, []).append(f"External Work: #{num}")

    for pr in open_prs_data:
        author = pr.get("author", {}).get("login", "") if pr.get("author") else ""
        num = pr["number"]
        url = pr["url"]
        for kind, item in kinds_in_tracker.items():
            if kind in pr["title"] and not is_bot_or_tracked(author, url, kind, item.get("trackingIssue", "")):
                external_works_by_kind.setdefault(kind, []).append(f"External Work: #{num}")

    # Process each resource in tracker data
    print("Reconciling tracking statuses with ground truth in code and GitHub...")
    for item in data:
        group = item["group"]
        kind = item["kind"]
        version = item["version"]
        kind_lower = kind.lower()

        is_registered = kind in registered_kinds
        open_migration_issue = open_migration_issues_by_kind.get(kind)
        closed_migration_issue = closed_migration_issues_by_kind.get(kind)

        # Step 2: Registered controllers are ALWAYS Completed
        if is_registered:
            item["state"] = "Completed"
            item["trackingIssue"] = ""
            item["assignee"] = ""
            item["stage"] = "Stage 5 (Controller Implemented)"
            item["steps"] = {
                "gen-types": True,
                "identity-reference": True,
                "mapper-fuzzer": True,
                "mocks": True,
                "controller": True,
                "tests": True
            }
        else:
            # Controller is NOT registered in code -> Cannot be Completed
            has_active_issue = open_migration_issue is not None
            has_work = check_any_work_detected(group, kind_lower, has_active_issue)

            # Revert to In Progress or Not Started
            if item["state"] == "Completed":
                print(f"Reverting state for Kind: {kind} as it is NOT registered in static_config.go")
                item["state"] = "In Progress" if has_work else "Not Started"

            # Check if there is an active tracking issue we should link
            if has_active_issue:
                item["state"] = "In Progress"
                item["trackingIssue"] = open_migration_issue["url"]
                item["assignee"] = open_migration_issue["assignees"][0]["login"] if open_migration_issue["assignees"] else ""
            else:
                # If there are external works on this kind, mark as In Progress
                ext_works = external_works_by_kind.get(kind, [])
                if ext_works and item["state"] == "Not Started":
                    item["state"] = "In Progress"

            # Check closed anomaly
            closed_anomaly = None
            if closed_migration_issue and not is_registered and not has_active_issue:
                # If closed but not registered, and no active issue, flag it
                closed_anomaly = f"Tracking issue #{closed_migration_issue['number']} is closed but direct controller is not registered in code"

            # Determine steps booleans for In Progress resources
            s1 = check_stage1(group, kind_lower)
            s2 = check_stage2(group, kind_lower)
            s3 = check_stage3(group, kind_lower)
            s4 = check_stage4(group, kind_lower)
            s5 = check_stage5(group, kind_lower)

            item["steps"] = {
                "gen-types": s1,
                "identity-reference": s2,
                "mapper-fuzzer": s3,
                "mocks": s4,
                "controller": s5,
                "tests": s4 # Stage 4 covers both mockgcp and tests
            }

            # Determine Stage String
            if s5:
                item["stage"] = "Stage 5 (Controller Implemented)"
            elif s4:
                item["stage"] = "Stage 4 (MockGCP/E2E Fixtures)"
            elif s3:
                item["stage"] = "Stage 3 (KRM Fuzzer)"
            elif s2:
                item["stage"] = "Stage 2 (Identity & Reference Types)"
            elif s1:
                item["stage"] = "Stage 1 (Direct KRM Types)"
            else:
                item["stage"] = "Investigation/Setup"

            # Determine notes
            missing_files = (not s2) and s1 # Has types but missing reference/identity stubs
            ext_works = external_works_by_kind.get(kind, [])
            item["notes"] = merge_notes_helper(item.get("notes", ""), missing_files, closed_anomaly, ext_works)

    # Re-map tracker dictionary with updated item states
    kinds_in_tracker = {item["kind"]: item for item in data}

    # Step 5: Identify Next Pending Resources
    print("Identifying unblocked pending resources (candidates with all dependencies completed)...")
    pending_candidates = []
    for item in data:
        if item["state"] == "Not Started" and item["defaultController"] in ("Terraform", "DCL"):
            deps_all_completed = True
            for dep in item.get("dependencies", []):
                dep_item = kinds_in_tracker.get(dep)
                if dep_item and dep_item["state"] != "Completed":
                    deps_all_completed = False
                    break
            if deps_all_completed:
                pending_candidates.append(item)

    # Sort candidates by sortOrder ascending
    pending_candidates.sort(key=lambda x: x.get("sortOrder", 9999))
    print(f"Found {len(pending_candidates)} pending and unblocked resources.")

    # Save local tracking data to disk
    print(f"Saving updated tracker data to {tracker_filepath}...")
    save_data(tracker_filepath, data)

    # Calculate High-Level Status counts
    completed_count = sum(1 for item in data if item["state"] == "Completed")
    in_progress_count = sum(1 for item in data if item["state"] == "In Progress")
    pending_count = sum(1 for item in data if item["state"] == "Not Started")
    total_count = len(data)

    print(f"Counts: Completed={completed_count}, In Progress={in_progress_count}, Pending={pending_count}, Total={total_count}")

    # Step 7: Construct Progress Summary Comment
    summary_body = "### Migration Progress Tracker Summary\n\n"
    summary_body += "## High-Level Status\n"
    summary_body += "| State | Count |\n"
    summary_body += "|-------|-------|\n"
    summary_body += f"| Completed | {completed_count} |\n"
    summary_body += f"| In Progress | {in_progress_count} |\n"
    summary_body += f"| Pending | {pending_count} |\n"
    summary_body += f"| Total | {total_count} |\n\n"

    # In Progress Resources
    summary_body += "## In Progress Resources\n"
    summary_body += "| Kind | Current Stage | Tracking Issue/PR | Assignee | Notes |\n"
    summary_body += "|------|---------------|-------------------|----------|-------|\n"
    
    in_progress_list = [item for item in data if item["state"] == "In Progress"]
    in_progress_list.sort(key=lambda x: x["kind"])
    
    def format_tracking_issue(url):
        if not url:
            return "N/A"
        match = re.search(r"/issues/(\d+)", url)
        if match:
            return f"[#{match.group(1)}]({url})"
        match_pr = re.search(r"/pull/(\d+)", url)
        if match_pr:
            return f"[#{match_pr.group(1)}]({url})"
        return f"[Link]({url})"

    for item in in_progress_list:
        kind = item["kind"]
        stage = item["stage"]
        tracking_issue = format_tracking_issue(item.get("trackingIssue", ""))
        assignee = item.get("assignee", "")
        notes = item.get("notes", "")
        summary_body += f"| {kind} | {stage} | {tracking_issue} | {assignee} | {notes} |\n"

    summary_body += "\n"

    # Next Pending Resources
    summary_body += "## Next Resources (Pending & Unblocked)\n"
    summary_body += "| Kind | Sort Order | Default Controller | Dependencies | Notes |\n"
    summary_body += "|------|------------|--------------------|--------------|-------|\n"
    
    for item in pending_candidates:
        kind = item["kind"]
        sort_order = item["sortOrder"]
        ctrl = item["defaultController"]
        deps = ", ".join(item.get("dependencies", []))
        notes = item.get("notes", "")
        summary_body += f"| {kind} | {sort_order} | {ctrl} | {deps} | {notes} |\n"

    summary_body += "\n"

    # Completed Resources
    summary_body += "## Completed Resources\n"
    summary_body += "| Kind | Default Controller | Date Completed / Notes |\n"
    summary_body += "|------|--------------------|------------------------|\n"
    
    completed_list = [item for item in data if item["state"] == "Completed"]
    completed_list.sort(key=lambda x: x["kind"])
    
    for item in completed_list:
        kind = item["kind"]
        ctrl = item["defaultController"]
        summary_body += f"| {kind} | {ctrl} | Registered in code |\n"

    # Update or create Github comment
    print("Finding dynamic comment ID for the Migration Progress Tracker Summary on issue 10588...")
    comments_cmd = [
        "gh", "api", f"repos/GoogleCloudPlatform/k8s-config-connector/issues/{issue_number}/comments"
    ]
    comments_data = json.loads(subprocess.check_output(comments_cmd).decode("utf-8"))

    target_comment_id = None
    for comment in comments_data:
        if "### Migration Progress Tracker Summary" in comment["body"]:
            target_comment_id = comment["id"]
            break

    payload = {"body": summary_body}
    temp_json_path = "dev/migration-tracker/comment_body.json"
    with open(temp_json_path, "w") as tf:
        json.dump(payload, tf)

    if target_comment_id:
        print(f"Found existing summary comment with ID: {target_comment_id}. Editing via gh api PATCH...")
        edit_cmd = [
            "gh", "api", "-X", "PATCH",
            f"repos/GoogleCloudPlatform/k8s-config-connector/issues/comments/{target_comment_id}",
            "--input", temp_json_path
        ]
        subprocess.run(edit_cmd, check=True)
        print("Summary comment updated successfully via PATCH!")
    else:
        print("No existing summary comment found. Creating new comment via gh api POST...")
        create_cmd = [
            "gh", "api", "-X", "POST",
            f"repos/GoogleCloudPlatform/k8s-config-connector/issues/{issue_number}/comments",
            "--input", temp_json_path
        ]
        subprocess.run(create_cmd, check=True)
        print("Summary comment created successfully via POST!")

if __name__ == "__main__":
    main()
