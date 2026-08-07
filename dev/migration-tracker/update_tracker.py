#!/usr/bin/env python3
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
        tracker_data = json.load(f)

    all_kinds = [item["kind"] for item in tracker_data]
    print(f"Loaded {len(all_kinds)} kinds from data.json.")

    # Step 2: Audit Ground Reality in Code (Source of Truth)
    # Parse static_config.go to find registered direct controllers
    direct_registered_kinds = set()
    with open(STATIC_CONFIG_PATH, "r") as f:
        static_config_content = f.read()

    entry_pattern = re.compile(r'Group:\s*"([^"]+)",\s*Kind:\s*"([^"]+)"')
    for line in static_config_content.splitlines():
        match = entry_pattern.search(line)
        if match:
            group, kind = match.groups()
            if "ReconcilerTypeDirect" in line:
                direct_registered_kinds.add(kind)

    print(f"Parsed {len(direct_registered_kinds)} registered direct controller kinds from static_config.go.")

    # Step 3: Scan GitHub for Active and External Work (SET 1 & SET 2)
    # 1. Search for Active Migration Workflows/Issues (SET 1)
    print("Fetching active migration workflow issues...")
    issues_json = run_command([
        "gh", "issue", "list", "--state", "all",
        "--label", "overseer,workflow/migrate",
        "--json", "number,title,labels,assignees,createdAt,state,url"
    ])
    migration_issues = json.loads(issues_json)
    print(f"Found {len(migration_issues)} migration workflow issues.")

    # Extract Kind -> issue info mapping
    migration_by_kind = {}
    for issue in migration_issues:
        title = issue.get("title", "")
        if "TRACKER:" in title:
            continue
        m = re.search(r"Migrat(?:e|ing|ion)\s+([A-Za-z0-9]+)", title, re.IGNORECASE)
        if m:
            kind = m.group(1)
            # Check if this is a known kind in the tracker
            if kind in all_kinds:
                if kind not in migration_by_kind:
                    migration_by_kind[kind] = []
                migration_by_kind[kind].append(issue)

    # 2. Search for Other/External Issues and PRs (SET 2)
    print("Fetching all open issues and PRs in bulk for SET 2...")
    open_issues_json = run_command([
        "gh", "issue", "list", "--state", "open", "--limit", "2000",
        "--json", "number,title,body,url,assignees,author,state"
    ])
    open_prs_json = run_command([
        "gh", "pr", "list", "--state", "open", "--limit", "2000",
        "--json", "number,title,body,url,author,state"
    ])
    
    open_issues = json.loads(open_issues_json)
    open_prs = json.loads(open_prs_json)
    print(f"Loaded {len(open_issues)} open issues and {len(open_prs)} open PRs from GitHub.")

    # Combine issues and PRs
    all_open_items = []
    for item in open_issues:
        item["is_pr"] = False
        all_open_items.append(item)
    for item in open_prs:
        item["is_pr"] = True
        all_open_items.append(item)

    # Pre-map tracking issues of resources to avoid recording them as external work
    tracking_issue_numbers = set()
    for kind, issues in migration_by_kind.items():
        for issue in issues:
            tracking_issue_numbers.add(issue["number"])

    # Local substring matching of Kinds to titles/bodies for SET 2
    external_work_by_kind = {}
    for item in all_open_items:
        # Filter out bots
        author = item.get("author") or {}
        author_login = author.get("login", "")
        if "bot" in author_login.lower() or "robot" in author_login.lower():
            continue
        
        number = item.get("number")
        if number in tracking_issue_numbers:
            continue

        title = item.get("title", "")
        body = item.get("body", "") or ""

        # Find all Kind names matching in title or body
        matched_kinds = []
        for kind in all_kinds:
            if kind in title or kind in body:
                matched_kinds.append(kind)

        # Filter out substrings (e.g. StorageBucket matching within StorageBucketAccessControl)
        final_matched_kinds = []
        for k in matched_kinds:
            is_sub = False
            for other in matched_kinds:
                if other != k and k in other:
                    k_count_title = title.count(k)
                    other_count_title = title.count(other)
                    k_count_body = body.count(k)
                    other_count_body = body.count(other)
                    if k_count_title == other_count_title and k_count_body == other_count_body:
                        is_sub = True
                        break
            if not is_sub:
                final_matched_kinds.append(k)

        for k in final_matched_kinds:
            if k not in external_work_by_kind:
                external_work_by_kind[k] = set()
            external_work_by_kind[k].add(number)

    print(f"Mapped external work for {len(external_work_by_kind)} kinds.")

    # Step 4: Determine Current Stage for In Progress Resources
    # We will compute the stage for each resource dynamically.
    def get_highest_stage(service, version, kind, ext_issues):
        dir_path = f"pkg/controller/direct/{service}"
        
        # Check Stage 5 (Controller Implemented)
        has_controller = False
        if os.path.exists(dir_path):
            files = os.listdir(dir_path)
            for f in files:
                fl = f.lower()
                if fl == "adapter.go" or fl == f"{kind.lower()}_controller.go" or fl == f"{kind.lower()}controller.go":
                    has_controller = True
                    break

        # Check Stage 4 (MockGCP/E2E Fixtures)
        has_mock_or_e2e = False
        if os.path.exists(f"mockgcp/mock{service}"):
            has_mock_or_e2e = True
        else:
            if os.path.exists(dir_path):
                for f in os.listdir(dir_path):
                    if f.endswith("_test.go"):
                        has_mock_or_e2e = True
                        break
            basic_dir = "pkg/test/resourcefixture/testdata/basic"
            if os.path.exists(basic_dir):
                for root, dirs, filenames in os.walk(basic_dir):
                    path_parts = [p.lower() for p in root.split(os.sep)]
                    if kind.lower() in path_parts:
                        has_mock_or_e2e = True
                        break

        # Check Stage 3 (KRM Fuzzer)
        has_fuzzer = False
        if os.path.exists(dir_path):
            for f in os.listdir(dir_path):
                fl = f.lower()
                if fl == f"{kind.lower()}_fuzzer.go" or fl == f"{kind.lower()}fuzzer.go":
                    has_fuzzer = True
                    break

        # Check Stage 2 (Identity & Reference Types)
        apis_path = f"apis/{service}/{version}"
        has_identity_ref = False
        if os.path.exists(apis_path):
            for f in os.listdir(apis_path):
                fl = f.lower()
                if fl in [f"{kind.lower()}_identity.go", f"{kind.lower()}_reference.go"]:
                    has_identity_ref = True
                    break

        # Check Stage 1 (Direct KRM Types)
        has_types = False
        if os.path.exists(apis_path):
            for f in os.listdir(apis_path):
                fl = f.lower()
                if fl == f"{kind.lower()}_types.go":
                    has_types = True
                    break

        matched_stages = [0]
        if has_types:
            matched_stages.append(1)
        if has_identity_ref:
            matched_stages.append(2)
        if has_fuzzer:
            matched_stages.append(3)
        if has_mock_or_e2e:
            matched_stages.append(4)
        if has_controller:
            matched_stages.append(5)

        max_stage_num = max(matched_stages)

        # Inspect titles of external issues/PRs to infer stage if max_stage_num is 0
        if max_stage_num == 0 and ext_issues:
            # Look at titles of those issues/PRs
            all_associated_items = [x for x in all_open_items if x["number"] in ext_issues]
            for item in all_associated_items:
                t_lower = item.get("title", "").lower()
                if "controller" in t_lower or "reconcil" in t_lower:
                    max_stage_num = max(max_stage_num, 5)
                elif "mock" in t_lower or "test" in t_lower or "fixture" in t_lower:
                    max_stage_num = max(max_stage_num, 4)
                elif "fuzzer" in t_lower:
                    max_stage_num = max(max_stage_num, 3)
                elif "identity" in t_lower or "reference" in t_lower or "ref" in t_lower:
                    max_stage_num = max(max_stage_num, 2)
                elif "types" in t_lower or "krm" in t_lower:
                    max_stage_num = max(max_stage_num, 1)

        stage_names = {
            5: "Stage 5 (Controller Implemented)",
            4: "Stage 4 (MockGCP/E2E Fixtures)",
            3: "Stage 3 (KRM Fuzzer)",
            2: "Stage 2 (Identity & Reference Types)",
            1: "Stage 1 (Direct KRM Types)",
            0: "Investigation/Setup"
        }
        return stage_names[max_stage_num], {
            "gen-types": has_types,
            "identity-reference": has_identity_ref,
            "mapper-fuzzer": has_fuzzer,
            "mocks": os.path.exists(f"mockgcp/mock{service}"),
            "controller": has_controller,
            "tests": has_mock_or_e2e
        }

    # Now let's loop and process all tracker items!
    updated_tracker_data = []
    completed_kinds = set()

    for item in tracker_data:
        kind = item["kind"]
        service = item["group"]
        version = item["version"]

        ext_issues = list(external_work_by_kind.get(kind, []))

        # Check if the direct controller is registered in code
        is_registered = kind in direct_registered_kinds

        if is_registered:
            # Step 2.2: Direct controller is registered
            item["state"] = "Completed"
            item["steps"] = {
                "gen-types": True,
                "identity-reference": True,
                "mapper-fuzzer": True,
                "mocks": True,
                "controller": True,
                "tests": True
            }
            item["trackingIssue"] = ""
            item["assignee"] = ""
            item["stage"] = "Stage 5 (Controller Implemented)"
            item["notes"] = ""
            completed_kinds.add(kind)
        else:
            # Step 2.3: Direct controller is NOT registered
            # Ensure it is not marked Completed
            if item.get("state") == "Completed":
                print(f"Reverting {kind} from Completed to In Progress/Not Started as it is not registered in static_config.go")
                item["state"] = "In Progress"

            # Check if there is a tracking issue (from overseer issues)
            has_tracking_issue = kind in migration_by_kind
            tracking_info = None
            if has_tracking_issue:
                # Find the open one or latest one
                kind_issues = migration_by_kind[kind]
                open_issues = [i for i in kind_issues if i["state"].upper() == "OPEN"]
                if open_issues:
                    tracking_info = open_issues[0]
                else:
                    tracking_info = kind_issues[0] # closed one

            # Determine dynamic stage
            computed_stage, dynamic_steps = get_highest_stage(service, version, kind, ext_issues)
            item["stage"] = computed_stage
            
            # Check if work is detected (either highest stage is > 0, or we have open external issues, or an open tracking issue)
            is_work_detected = (computed_stage != "Investigation/Setup") or ext_issues or (tracking_info and tracking_info["state"].upper() == "OPEN")

            if is_work_detected:
                item["state"] = "In Progress"
                item["steps"] = dynamic_steps
            else:
                item["state"] = "Not Started"
                item["steps"] = {
                    "gen-types": False,
                    "identity-reference": False,
                    "mapper-fuzzer": False,
                    "mocks": os.path.exists(f"mockgcp/mock{service}"),
                    "controller": False,
                    "tests": False
                }

            # Set tracking issue/assignee
            if tracking_info and tracking_info["state"].upper() == "OPEN":
                num = tracking_info["number"]
                url = tracking_info["url"]
                item["trackingIssue"] = f"[#{num}]({url})"
                
                assignees = tracking_info.get("assignees") or []
                if assignees:
                    item["assignee"] = assignees[0]["login"]
                else:
                    item["assignee"] = ""
            else:
                item["trackingIssue"] = "N/A"
                item["assignee"] = ""

            # Update notes
            notes_str = item.get("notes") or ""
            # Handle anomaly for closed tracking issue if direct not registered
            anomaly_str = ""
            if tracking_info and tracking_info["state"].upper() == "CLOSED":
                num = tracking_info["number"]
                anomaly_str = f"Tracking issue #{num} is closed but direct controller is not registered in code"

            # Remove previous "Tracking issue #... is closed but direct controller..." from notes_str
            notes_str = re.sub(r"Tracking issue #\d+ is closed but direct controller is not registered in code", "", notes_str)
            
            # Re-compile notes parts
            notes_parts = []
            for part in re.split(r',\s*', notes_str):
                p = part.strip()
                if p and not p.startswith("External Work: #") and not p.startswith("Community PR:"):
                    notes_parts.append(p)

            if anomaly_str:
                notes_parts.insert(0, anomaly_str)

            # Append external work
            for ext_num in sorted(ext_issues):
                notes_parts.append(f"External Work: #{ext_num}")

            item["notes"] = ", ".join(notes_parts)

        updated_tracker_data.append(item)

    # Save local tracking data to data.json
    with open(DATA_JSON_PATH, "w") as f:
        json.dump(updated_tracker_data, f, indent=2)
    print("Saved updated tracking data to dev/migration-tracker/data.json.")

    # Step 5: Identify Next Pending Resources
    # Next migration candidates criteria:
    # - "state" == "Not Started"
    # - "defaultController" is "Terraform" or "DCL"
    # - All listed "dependencies" have "state" == "Completed" in dev/migration-tracker/data.json
    # Sort these candidates by "sortOrder" ascending.
    dependency_states = {item["kind"]: item["state"] for item in updated_tracker_data}

    next_pending_resources = []
    for item in updated_tracker_data:
        if item["state"] == "Not Started" and item["defaultController"] in ["Terraform", "DCL"]:
            # Check dependencies
            deps = item.get("dependencies") or []
            all_deps_completed = True
            for dep in deps:
                # If dependency is in the tracker, it must be Completed
                if dep in dependency_states:
                    if dependency_states[dep] != "Completed":
                        all_deps_completed = False
                        break
            if all_deps_completed:
                next_pending_resources.append(item)

    # Sort candidates by "sortOrder" ascending
    next_pending_resources.sort(key=lambda x: x["sortOrder"])
    print(f"Identified {len(next_pending_resources)} next pending (unblocked) resources.")

    # Step 7: Update Summary Comment on Coordinator Issue
    # Build statistics
    completed_count = sum(1 for item in updated_tracker_data if item["state"] == "Completed")
    in_progress_count = sum(1 for item in updated_tracker_data if item["state"] == "In Progress")
    pending_count = sum(1 for item in updated_tracker_data if item["state"] == "Not Started")
    total_count = len(updated_tracker_data)

    print(f"Stats - Completed: {completed_count}, In Progress: {in_progress_count}, Pending: {pending_count}, Total: {total_count}")

    # Build In Progress Resources list (sorted by kind ascending)
    in_progress_resources = [item for item in updated_tracker_data if item["state"] == "In Progress"]
    in_progress_resources.sort(key=lambda x: x["kind"])

    # Build Completed Resources list (sorted by kind ascending)
    completed_resources = [item for item in updated_tracker_data if item["state"] == "Completed"]
    completed_resources.sort(key=lambda x: x["kind"])

    # Build summary body markdown
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
    for r in in_progress_resources:
        kind = r["kind"]
        stage = r["stage"]
        tracking = r.get("trackingIssue") or "N/A"
        assignee = r.get("assignee") or ""
        notes = r.get("notes") or ""
        summary_lines.append(f"| {kind} | {stage} | {tracking} | {assignee} | {notes} |")
    summary_lines.append("")

    summary_lines.append("## Next Resources (Pending & Unblocked)")
    summary_lines.append("| Kind | Sort Order | Default Controller | Dependencies | Notes |")
    summary_lines.append("|------|------------|--------------------|--------------|-------|")
    for r in next_pending_resources:
        kind = r["kind"]
        sort_order = r["sortOrder"]
        controller = r["defaultController"]
        deps = ", ".join(r.get("dependencies", []))
        notes = r.get("notes") or ""
        summary_lines.append(f"| {kind} | {sort_order} | {controller} | {deps} | {notes} |")
    summary_lines.append("")

    summary_lines.append("## Completed Resources")
    summary_lines.append("| Kind | Default Controller | Date Completed / Notes |")
    summary_lines.append("|------|--------------------|------------------------|")
    for r in completed_resources:
        kind = r["kind"]
        controller = r["defaultController"]
        summary_lines.append(f"| {kind} | {controller} | Registered in code |")
    summary_lines.append("")

    summary_body = "\n".join(summary_lines)

    # Search for an existing tracker comment on the coordinator issue
    # We already fetched issue comments using: gh issue view 10588 --json comments
    # Let's find the comment ID of the comment containing TRACKING_COMMENT_HEADER
    comments_list = json.loads(run_command(["gh", "issue", "view", COORDINATOR_ISSUE_NUMBER, "--json", "comments"]))["comments"]
    
    tracking_comment_url = None
    for comment in reversed(comments_list):
        if TRACKING_COMMENT_HEADER in comment.get("body", ""):
            tracking_comment_url = comment.get("url", "")
            break

    # Extract db_id from tracking_comment_url
    db_id = None
    if tracking_comment_url:
        m = re.search(r"issuecomment-(\d+)", tracking_comment_url)
        if m:
            db_id = m.group(1)

    if db_id:
        print(f"Found existing tracker comment with DB ID: {db_id}. Editing it...")
        # Write body to a temp file to avoid argument length limits or shell expansion issues
        with open("summary_body.md", "w") as f:
            f.write(summary_body)
        run_command(["gh", "api", "-X", "PATCH", f"repos/{{owner}}/{{repo}}/issues/comments/{db_id}", "-F", "body=@summary_body.md"])
        os.remove("summary_body.md")
        print("Successfully updated the existing coordinator issue comment.")
    else:
        print("No existing tracker comment found. Creating a new one...")
        with open("summary_body.md", "w") as f:
            f.write(summary_body)
        run_command(["gh", "api", f"repos/{{owner}}/{{repo}}/issues/{COORDINATOR_ISSUE_NUMBER}/comments", "-F", "body=@summary_body.md"])
        os.remove("summary_body.md")
        print("Successfully created a new coordinator issue comment.")

if __name__ == "__main__":
    main()
