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

import json
import re
import os
import sys
import subprocess

COORDINATOR_ISSUE_NUMBER = 10588
DATA_JSON_PATH = "dev/migration-tracker/data.json"
STATIC_CONFIG_PATH = "pkg/controller/resourceconfig/static_config.go"

def file_exists(path):
    return os.path.isfile(path)

def dir_exists(path):
    return os.path.isdir(path)

def any_file_in_dir(dir_path, suffix=None, contains=None):
    if not dir_exists(dir_path):
        return False
    try:
        for f in os.listdir(dir_path):
            if suffix and f.lower().endswith(suffix.lower()):
                return True
            if contains and contains.lower() in f.lower():
                return True
    except Exception:
        pass
    return False

def determine_stage(group, kind, version):
    g_low = group.lower()
    k_low = kind.lower()
    v_low = version.lower()
    
    suffix = k_low
    if k_low.startswith(g_low) and len(k_low) > len(g_low):
        suffix = k_low[len(g_low):]
        
    # Stage 5 checks
    stage5_files = [
        f"pkg/controller/direct/{g_low}/{k_low}_controller.go",
        f"pkg/controller/direct/{g_low}/{suffix}_controller.go",
        f"pkg/controller/direct/{k_low}/{k_low}_controller.go",
        f"pkg/controller/direct/{g_low}/adapter.go",
        f"pkg/controller/direct/{k_low}/adapter.go",
        f"pkg/controller/direct/{g_low}/controller.go",
        f"pkg/controller/direct/{k_low}/controller.go"
    ]
    if any(file_exists(f) for f in stage5_files):
        return "Stage 5 (Controller Implemented)"
        
    # Stage 4 checks
    mockgcp_dirs = [
        f"mockgcp/mock{g_low}",
        f"mockgcp/mock{k_low}"
    ]
    if any(dir_exists(d) for d in mockgcp_dirs):
        return "Stage 4 (MockGCP/E2E Fixtures)"
        
    direct_dirs = [
        f"pkg/controller/direct/{g_low}",
        f"pkg/controller/direct/{k_low}"
    ]
    for d in direct_dirs:
        if any_file_in_dir(d, contains="test"):
            return "Stage 4 (MockGCP/E2E Fixtures)"
            
    # Stage 3 checks
    stage3_files = [
        f"pkg/controller/direct/{g_low}/{k_low}_fuzzer.go",
        f"pkg/controller/direct/{g_low}/{suffix}_fuzzer.go",
        f"pkg/controller/direct/{k_low}/{k_low}_fuzzer.go"
    ]
    if any(file_exists(f) for f in stage3_files):
        return "Stage 3 (KRM Fuzzer)"
        
    # Stage 2 checks
    stage2_files = [
        f"apis/{g_low}/{v_low}/{k_low}_identity.go",
        f"apis/{g_low}/{v_low}/{k_low}_reference.go",
        f"apis/{g_low}/{v_low}/{suffix}_identity.go",
        f"apis/{g_low}/{v_low}/{suffix}_reference.go",
        f"apis/{k_low}/{v_low}/{k_low}_identity.go",
        f"apis/{k_low}/{v_low}/{k_low}_reference.go"
    ]
    if any(file_exists(f) for f in stage2_files):
        return "Stage 2 (Identity & Reference Types)"
        
    # Stage 1 checks
    stage1_files = [
        f"apis/{g_low}/{v_low}/{k_low}_types.go",
        f"apis/{g_low}/{v_low}/{suffix}_types.go",
        f"apis/{k_low}/{v_low}/{k_low}_types.go"
    ]
    if any(file_exists(f) for f in stage1_files):
        return "Stage 1 (Direct KRM Types)"
        
    return "Investigation/Setup"

def main():
    # Parse registered direct controllers from static_config.go
    direct_registered = set()
    re_mapping = re.compile(r'Group:\s*"([^"]+)"\s*,\s*Kind:\s*"([^"]+)"')
    with open(STATIC_CONFIG_PATH, "r") as f:
        for line in f:
            line_clean = line.split("//")[0].strip()
            if not line_clean:
                continue
            m = re_mapping.search(line_clean)
            if m:
                group = m.group(1).replace(".cnrm.cloud.google.com", "")
                kind = m.group(2)
                if "k8s.ReconcilerTypeDirect" in line_clean:
                    direct_registered.add((group, kind))

    # Read data.json
    with open(DATA_JSON_PATH, "r") as f:
        data = json.load(f)

    # Get migration tracker issues from GitHub
    cmd = ["gh", "issue", "list", "--state", "all", "--label", "overseer,workflow/migrate", "--json", "number,title,state,url,assignees", "--limit", "1000"]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    migration_issues = json.loads(res.stdout)

    migration_by_kind = {}
    for iss in migration_issues:
        title = iss["title"]
        m = re.search(r'(?:Migrate|Migrating)\s+(\w+)\s+(?:to|from)', title, re.IGNORECASE)
        if m:
            kind = m.group(1)
            is_migration = any(item["kind"] == kind for item in data)
            if is_migration:
                assignee = ""
                if iss.get("assignees"):
                    assignee = iss["assignees"][0]["login"]
                migration_by_kind[kind] = {
                    "number": iss["number"],
                    "url": iss["url"],
                    "state": iss["state"].upper(),
                    "assignee": assignee
                }

    # Get all open issues and PRs (excluding bots)
    cmd_iss = ["gh", "issue", "list", "--state", "open", "--limit", "1000", "--json", "number,title,url,author,state"]
    res_iss = subprocess.run(cmd_iss, capture_output=True, text=True, check=True)
    issues = json.loads(res_iss.stdout)
    
    cmd_pr = ["gh", "pr", "list", "--state", "open", "--limit", "1000", "--json", "number,title,url,author,state"]
    res_pr = subprocess.run(cmd_pr, capture_output=True, text=True, check=True)
    prs = json.loads(res_pr.stdout)
    
    all_open = issues + prs

    # Update states of kinds in data.json
    for item in data:
        group = item["group"]
        kind = item["kind"]
        version = item["version"]
        
        g_low = group.lower()
        k_low = kind.lower()
        v_low = version.lower()
        
        suffix = k_low
        if k_low.startswith(g_low) and len(k_low) > len(g_low):
            suffix = k_low[len(g_low):]

        is_registered_direct = (group, kind) in direct_registered
        
        if is_registered_direct:
            item["state"] = "Completed"
            item["steps"] = {
                "gen-types": True,
                "identity-reference": True,
                "mapper-fuzzer": True,
                "mocks": True,
                "controller": True,
                "tests": True
            }
            item["stage"] = "Stage 5 (Controller Implemented)"
            if "Direct" not in item["supportedControllers"]:
                item["supportedControllers"].append("Direct")
            # Reset assignee and tracking issue once Completed
            item["trackingIssue"] = ""
            item["assignee"] = ""
            item["notes"] = ""
        else:
            # Revert from Completed if it was
            if item["state"] == "Completed":
                stage = determine_stage(group, kind, version)
                if stage != "Investigation/Setup":
                    item["state"] = "In Progress"
                else:
                    item["state"] = "Not Started"
            
            # Determine stage of uncompleted resource
            stage = determine_stage(group, kind, version)
            item["stage"] = stage
            
            if stage != "Investigation/Setup" and item["state"] == "Not Started":
                item["state"] = "In Progress"
                
            # Set steps based on stage
            if stage == "Stage 5 (Controller Implemented)":
                item["steps"] = {"gen-types": True, "identity-reference": True, "mapper-fuzzer": True, "mocks": True, "controller": True, "tests": True}
            elif stage == "Stage 4 (MockGCP/E2E Fixtures)":
                item["steps"] = {"gen-types": True, "identity-reference": True, "mapper-fuzzer": True, "mocks": True, "controller": False, "tests": False}
            elif stage == "Stage 3 (KRM Fuzzer)":
                item["steps"] = {"gen-types": True, "identity-reference": True, "mapper-fuzzer": True, "mocks": False, "controller": False, "tests": False}
            elif stage == "Stage 2 (Identity & Reference Types)":
                item["steps"] = {"gen-types": True, "identity-reference": True, "mapper-fuzzer": False, "mocks": False, "controller": False, "tests": False}
            elif stage == "Stage 1 (Direct KRM Types)":
                item["steps"] = {"gen-types": True, "identity-reference": False, "mapper-fuzzer": False, "mocks": False, "controller": False, "tests": False}
            else:
                item["steps"] = {"gen-types": False, "identity-reference": False, "mapper-fuzzer": False, "mocks": False, "controller": False, "tests": False}
                
            # Process tracking issue (SET 1)
            tracking_iss = migration_by_kind.get(kind)
            if tracking_iss:
                if tracking_iss["state"] == "OPEN":
                    item["state"] = "In Progress"
                    item["trackingIssue"] = tracking_iss["url"]
                    item["assignee"] = tracking_iss["assignee"]
                else: # CLOSED
                    item["trackingIssue"] = ""
                    item["assignee"] = ""
            else:
                item["trackingIssue"] = ""
                item["assignee"] = ""

            # Build notes
            notes_list = []
            
            # 1. Missing _identity or _reference
            has_identity = any(file_exists(f) for f in [
                f"apis/{g_low}/{v_low}/{k_low}_identity.go",
                f"apis/{g_low}/{v_low}/{suffix}_identity.go",
                f"apis/{k_low}/{v_low}/{k_low}_identity.go"
            ])
            has_reference = any(file_exists(f) for f in [
                f"apis/{g_low}/{v_low}/{k_low}_reference.go",
                f"apis/{g_low}/{v_low}/{suffix}_reference.go",
                f"apis/{k_low}/{v_low}/{k_low}_reference.go"
            ])
            if stage in ["Stage 4 (MockGCP/E2E Fixtures)", "Stage 3 (KRM Fuzzer)", "Stage 2 (Identity & Reference Types)", "Stage 1 (Direct KRM Types)"]:
                if not (has_identity and has_reference):
                    notes_list.append("Missing _reference.go or _identity.go")
                    
            # 2. Closed tracking issue anomaly
            if tracking_iss and tracking_iss["state"] == "CLOSED":
                notes_list.append(f"Tracking issue #{tracking_iss['number']} is closed but direct controller is not registered in code")
                
            # 3. Community / External Work (SET 2)
            for ext in all_open:
                author_login = ext.get("author", {}).get("login", "")
                # Skip bots/robots
                if ext.get("author", {}).get("is_bot") or "bot" in author_login.lower() or "robot" in author_login.lower():
                    continue
                # Skip if already tracked
                if tracking_iss and ext["number"] == tracking_iss["number"]:
                    continue
                # Check for kind in title
                if re.search(r'\b' + re.escape(kind) + r'\b', ext["title"], re.IGNORECASE):
                    notes_list.append(f"External Work: #{ext['number']}")
                    item["state"] = "In Progress"
                    
            item["notes"] = ", ".join(notes_list)

    # Save data.json
    with open(DATA_JSON_PATH, "w") as f:
        json.dump(data, f, indent=2)

    # Calculate metrics
    completed_count = sum(1 for item in data if item["state"] == "Completed")
    in_progress_count = sum(1 for item in data if item["state"] == "In Progress")
    pending_count = sum(1 for item in data if item["state"] == "Not Started")
    total_count = len(data)

    # Step 5: Identify Next Pending Resources
    # Build states map
    states_map = {item["kind"]: item["state"] for item in data}
    next_resources = []
    for item in data:
        if item["state"] == "Not Started" and item["defaultController"] in ["Terraform", "DCL"]:
            # Check dependencies
            deps_all_completed = True
            for dep in item.get("dependencies", []):
                # If dependency exists, check if it is Completed
                if dep in states_map and states_map[dep] != "Completed":
                    deps_all_completed = False
                    break
            if deps_all_completed:
                next_resources.append(item)
                
    # Sort next candidates by sortOrder ascending
    next_resources.sort(key=lambda x: x["sortOrder"])

    # Generate Markdown Summary Comment
    # Build In Progress Resources Table
    in_progress_rows = []
    in_progress_items = [item for item in data if item["state"] == "In Progress"]
    # Sort In Progress by Kind alphabetically
    in_progress_items.sort(key=lambda x: x["kind"])
    for item in in_progress_items:
        tracking_issue_md = "N/A"
        if item.get("trackingIssue"):
            iss_num = item["trackingIssue"].rstrip("/").split("/")[-1]
            tracking_issue_md = f"[#{iss_num}]({item['trackingIssue']})"
        in_progress_rows.append(f"| {item['kind']} | {item['stage']} | {tracking_issue_md} | {item['assignee']} | {item['notes']} |")

    # Build Next Resources Table
    next_rows = []
    for item in next_resources:
        deps_str = ", ".join(item.get("dependencies", []))
        next_rows.append(f"| {item['kind']} | {item['sortOrder']} | {item['defaultController']} | {deps_str} | {item['notes']} |")

    # Build Completed Resources Table
    completed_rows = []
    completed_items = [item for item in data if item["state"] == "Completed"]
    # Sort Completed by Kind alphabetically
    completed_items.sort(key=lambda x: x["kind"])
    for item in completed_items:
        completed_rows.append(f"| {item['kind']} | {item['defaultController']} | Registered in code |")

    summary_body = f"""### Migration Progress Tracker Summary

## High-Level Status
| State | Count |
|-------|-------|
| Completed | {completed_count} |
| In Progress | {in_progress_count} |
| Pending | {pending_count} |
| Total | {total_count} |

## In Progress Resources
| Kind | Current Stage | Tracking Issue/PR | Assignee | Notes |
|------|---------------|-------------------|----------|-------|
""" + "\n".join(in_progress_rows) + """

## Next Resources (Pending & Unblocked)
| Kind | Sort Order | Default Controller | Dependencies | Notes |
|------|------------|--------------------|--------------|-------|
""" + "\n".join(next_rows) + """

## Completed Resources
| Kind | Default Controller | Date Completed / Notes |
|------|--------------------|------------------------|
""" + "\n".join(completed_rows) + """
"""

    print("---SUMMARY_BODY_START---")
    print(summary_body)
    print("---SUMMARY_BODY_END---")

    # Save summary body to a temporary file so bash can easily fetch it
    with open("summary_comment.md", "w") as f:
        f.write(summary_body)

    # Post or Edit the comment on GitHub
    print("Fetching comments from coordinator issue...")
    cmd = ["gh", "issue", "view", str(COORDINATOR_ISSUE_NUMBER), "--json", "comments"]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    comments_data = json.loads(res.stdout) if res.stdout else {}
    comments_list = comments_data.get("comments", [])
    
    existing_comment_db_id = None
    for c in reversed(comments_list):
        if "### Migration Progress Tracker Summary" in c.get("body", ""):
            url = c.get("url", "")
            m = re.search(r'#issuecomment-(\d+)', url)
            if m:
                existing_comment_db_id = m.group(1)
            break
            
    if existing_comment_db_id:
        print(f"Found existing comment with DB ID {existing_comment_db_id}. Editing via gh issue comment...")
        comment_url = f"https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/{COORDINATOR_ISSUE_NUMBER}#issuecomment-{existing_comment_db_id}"
        subprocess.run(["gh", "issue", "comment", comment_url, "-F", "summary_comment.md"], check=True)
        print("Comment edited successfully!")
    else:
        print("No existing comment found. Creating new comment...")
        subprocess.run(["gh", "issue", "comment", str(COORDINATOR_ISSUE_NUMBER), "-F", "summary_comment.md"], check=True)
        print("Comment created successfully!")

if __name__ == "__main__":
    main()
