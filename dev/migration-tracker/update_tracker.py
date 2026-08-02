#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys

COORDINATOR_ISSUE = "10588"

def run_cmd(args):
    res = subprocess.run(args, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error running {' '.join(args)}: {res.stderr}")
        return ""
    return res.stdout

def parse_static_config():
    direct_kinds = set()
    with open("pkg/controller/resourceconfig/static_config.go", "r") as f:
        content = f.read()
    
    # Matching pattern of static registration line-by-line
    for line in content.splitlines():
        if "Group:" in line and "Kind:" in line:
            m = re.search(r'Kind:\s*"([^"]+)"', line)
            if m:
                kind = m.group(1)
                # Check if k8s.ReconcilerTypeDirect is in SupportedControllers
                if "k8s.ReconcilerTypeDirect" in line:
                    direct_kinds.add(kind)
    return direct_kinds

def check_stages(service, kind, version):
    lower_kind = kind.lower()
    
    # Stage 5 (Controller Implemented)
    stage5_files = [
        f"pkg/controller/direct/{service}/{lower_kind}_controller.go",
        f"pkg/controller/direct/{service}/adapter.go"
    ]
    has_stage5 = any(os.path.exists(f) for f in stage5_files)
    
    # Stage 4 (MockGCP/E2E Fixtures)
    has_stage4 = False
    service_dir = f"pkg/controller/direct/{service}"
    if os.path.exists(service_dir):
        for filename in os.listdir(service_dir):
            if filename.endswith("_test.go") or "test" in filename.lower() or "fixture" in filename.lower():
                has_stage4 = True
                break
    if os.path.exists(f"mockgcp/mock{service.lower()}") or os.path.exists(f"mockgcp/mock{service}"):
        has_stage4 = True
        
    # Stage 3 (KRM Fuzzer)
    has_stage3 = os.path.exists(f"pkg/controller/direct/{service}/{lower_kind}_fuzzer.go")
    
    # Stage 2 (Identity & Reference Types)
    has_stage2 = (
        os.path.exists(f"apis/{service}/{version}/{lower_kind}_identity.go") or
        os.path.exists(f"apis/{service}/{version}/{lower_kind}_reference.go")
    )
    
    # Stage 1 (Direct KRM Types)
    has_stage1 = os.path.exists(f"apis/{service}/{version}/{lower_kind}_types.go")
    
    has_identity = os.path.exists(f"apis/{service}/{version}/{lower_kind}_identity.go")
    has_reference = os.path.exists(f"apis/{service}/{version}/{lower_kind}_reference.go")
    
    if has_stage5:
        return "Stage 5 (Controller Implemented)", has_identity, has_reference
    if has_stage4:
        return "Stage 4 (MockGCP/E2E Fixtures)", has_identity, has_reference
    if has_stage3:
        return "Stage 3 (KRM Fuzzer)", has_identity, has_reference
    if has_stage2:
        return "Stage 2 (Identity & Reference Types)", has_identity, has_reference
    if has_stage1:
        return "Stage 1 (Direct KRM Types)", has_identity, has_reference
        
    return None, has_identity, has_reference

def main():
    direct_kinds = parse_static_config()
    print(f"Parsed {len(direct_kinds)} direct kinds from static_config.go")
    
    # Fetch overseer/workflow migration issues (SET 1)
    issues_str = run_cmd(["gh", "issue", "list", "--state", "all", "--label", "overseer,workflow/migrate", "--json", "number,title,state,url,assignees", "--limit", "500"])
    migration_issues = []
    if issues_str:
        migration_issues = json.loads(issues_str)
    print(f"Fetched {len(migration_issues)} migration issues")
    
    open_migration_issues = {}
    closed_migration_issues = {}
    for issue in migration_issues:
        title = issue.get("title", "")
        kind = None
        match1 = re.search(r'Migrate\s+([A-Za-z0-9_]+)\s+to\s+Direct', title, re.IGNORECASE)
        match2 = re.search(r'Migrating\s+([A-Za-z0-9_]+)\s+to\s+Direct', title, re.IGNORECASE)
        match3 = re.search(r'direct\s+controller\s+for\s+([A-Za-z0-9_]+)', title, re.IGNORECASE)
        if match1:
            kind = match1.group(1)
        elif match2:
            kind = match2.group(1)
        elif match3:
            kind = match3.group(1)
            
        if kind:
            if issue.get("state") == "OPEN":
                open_migration_issues[kind] = issue
            else:
                closed_migration_issues[kind] = issue
                
    # Fetch all open issues and PRs (SET 2)
    open_issues_str = run_cmd(["gh", "issue", "list", "--state", "open", "--limit", "1000", "--json", "number,title,url,assignees,author"])
    open_prs_str = run_cmd(["gh", "pr", "list", "--state", "open", "--limit", "1000", "--json", "number,title,url,author"])
    
    all_open_issues = json.loads(open_issues_str) if open_issues_str else []
    all_open_prs = json.loads(open_prs_str) if open_prs_str else []
    
    # Load data.json
    with open("dev/migration-tracker/data.json", "r") as f:
        data = json.load(f)
        
    print(f"Loaded {len(data)} resources from data.json")
    
    # Step 2: Mark registered direct kinds as Completed and sync other fields
    completed_kinds = set()
    for item in data:
        kind = item["kind"]
        if kind in direct_kinds:
            item["state"] = "Completed"
            # reset/populate completion steps
            for k in item["steps"]:
                item["steps"][k] = True
            if "Direct" not in item["supportedControllers"]:
                item["supportedControllers"].append("Direct")
            completed_kinds.add(kind)
        else:
            if item.get("state") == "Completed":
                # Revert if it was Completed but direct is not in static config
                service = item["group"]
                version = item["version"]
                highest_stage, _, _ = check_stages(service, kind, version)
                if highest_stage is not None:
                    item["state"] = "In Progress"
                else:
                    item["state"] = "Not Started"
                    
    # Sync In Progress and Not Started resources
    for item in data:
        kind = item["kind"]
        service = item["group"]
        version = item["version"]
        lower_kind = kind.lower()
        
        if kind in completed_kinds:
            continue
            
        highest_stage, has_identity, has_reference = check_stages(service, kind, version)
        
        tracking_issue = "N/A"
        assignee = ""
        is_overseer_open = False
        
        if kind in open_migration_issues:
            issue = open_migration_issues[kind]
            tracking_issue = f"[#{issue['number']}]({issue['url']})"
            is_overseer_open = True
            assignees = issue.get("assignees", [])
            if assignees:
                assignee = assignees[0].get("login", "")
            item["state"] = "In Progress"
            
        closed_issue_anomaly = ""
        if not is_overseer_open and kind in closed_migration_issues:
            issue = closed_migration_issues[kind]
            closed_issue_anomaly = f"Tracking issue #{issue['number']} is closed but direct controller is not registered in code"
            
        # External Work scan
        external_work = []
        for x in all_open_issues + all_open_prs:
            author_login = x.get("author", {}).get("login", "") if x.get("author") else ""
            if "bot" in author_login.lower() or "robot" in author_login.lower():
                continue
            if tracking_issue != "N/A" and str(x["number"]) in tracking_issue:
                continue
                
            title = x.get("title", "")
            if re.search(r'\b' + re.escape(kind) + r'\b', title):
                external_work.append(f"External Work: #{x['number']}")
                
        if external_work:
            item["state"] = "In Progress"
            
        if highest_stage is not None:
            item["state"] = "In Progress"
            
        if highest_stage is None and tracking_issue == "N/A" and not external_work:
            item["state"] = "Not Started"
            
        # Notes building
        notes_parts = []
        if item["state"] == "In Progress":
            if not has_identity and not has_reference:
                notes_parts.append("Missing _reference.go or _identity.go")
        if closed_issue_anomaly:
            notes_parts.append(closed_issue_anomaly)
        
        external_work = sorted(list(set(external_work)), key=lambda s: int(re.search(r'\d+', s).group()))
        for ext in external_work:
            notes_parts.append(ext)
            
        item["trackingIssue"] = tracking_issue
        item["assignee"] = assignee
        item["notes"] = ", ".join(notes_parts)
        
        if highest_stage:
            item["stage"] = highest_stage
        else:
            item["stage"] = "Investigation/Setup"
            
        stage5_files = [
            f"pkg/controller/direct/{service}/{lower_kind}_controller.go",
            f"pkg/controller/direct/{service}/adapter.go"
        ]
        item["steps"]["gen-types"] = os.path.exists(f"apis/{service}/{version}/{lower_kind}_types.go")
        item["steps"]["identity-reference"] = (
            os.path.exists(f"apis/{service}/{version}/{lower_kind}_identity.go") or
            os.path.exists(f"apis/{service}/{version}/{lower_kind}_reference.go")
        )
        item["steps"]["mapper-fuzzer"] = os.path.exists(f"pkg/controller/direct/{service}/{lower_kind}_fuzzer.go")
        item["steps"]["controller"] = any(os.path.exists(f) for f in stage5_files)
        
    # Save the updated data.json back
    with open("dev/migration-tracker/data.json", "w") as f:
        json.dump(data, f, indent=2)
    print("Saved updated data.json")
    
    # Calculate counts
    completed_count = sum(1 for item in data if item["state"] == "Completed")
    in_progress_count = sum(1 for item in data if item["state"] == "In Progress")
    pending_count = sum(1 for item in data if item["state"] == "Not Started")
    total_count = len(data)
    
    # Identify Next Pending Resources (Step 5)
    pending_resources = []
    for item in data:
        if item["state"] == "Not Started":
            if item["defaultController"] in ["Terraform", "DCL"]:
                all_deps_completed = True
                for dep in item.get("dependencies", []):
                    dep_item = next((x for x in data if x["kind"] == dep), None)
                    if dep_item and dep_item["state"] != "Completed":
                        all_deps_completed = False
                        break
                if all_deps_completed:
                    pending_resources.append(item)
                    
    pending_resources.sort(key=lambda x: x["sortOrder"])
    
    # Build In Progress Resources Table
    in_progress_resources = [x for x in data if x["state"] == "In Progress"]
    in_progress_resources.sort(key=lambda x: x["kind"])
    
    # Build Completed Resources Table
    completed_resources_list = [x for x in data if x["state"] == "Completed"]
    completed_resources_list.sort(key=lambda x: x["kind"])
    
    # Generate Comment body
    body = "### Migration Progress Tracker Summary\n\n"
    body += "## High-Level Status\n"
    body += "| State | Count |\n"
    body += "|-------|-------|\n"
    body += f"| Completed | {completed_count} |\n"
    body += f"| In Progress | {in_progress_count} |\n"
    body += f"| Pending | {pending_count} |\n"
    body += f"| Total | {total_count} |\n\n"
    
    body += "## In Progress Resources\n"
    body += "| Kind | Current Stage | Tracking Issue/PR | Assignee | Notes |\n"
    body += "|------|---------------|-------------------|----------|-------|\n"
    for x in in_progress_resources:
        tracking = x["trackingIssue"] if x["trackingIssue"] != "" else "N/A"
        body += f"| {x['kind']} | {x['stage']} | {tracking} | {x['assignee']} | {x['notes']} |\n"
    body += "\n"
    
    body += "## Next Resources (Pending & Unblocked)\n"
    body += "| Kind | Sort Order | Default Controller | Dependencies | Notes |\n"
    body += "|------|------------|--------------------|--------------|-------|\n"
    for x in pending_resources:
        deps = ", ".join(x.get("dependencies", []))
        body += f"| {x['kind']} | {x['sortOrder']} | {x['defaultController']} | {deps} | {x['notes']} |\n"
    body += "\n"
    
    body += "## Completed Resources\n"
    body += "| Kind | Default Controller | Date Completed / Notes |\n"
    body += "|------|--------------------|------------------------|\n"
    for x in completed_resources_list:
        body += f"| {x['kind']} | {x['defaultController']} | Registered in code |\n"
        
    print(f"\nGenerated comment size: {len(body)} chars")
    
    # Post or Edit the comment on GitHub
    comments_str = run_cmd(["gh", "issue", "view", COORDINATOR_ISSUE, "--json", "comments"])
    existing_comment_id = None
    existing_comment_db_id = None
    if comments_str:
        comments_data = json.loads(comments_str)
        comments_list = comments_data.get("comments", [])
        for c in reversed(comments_list):
            if "### Migration Progress Tracker Summary" in c.get("body", ""):
                existing_comment_id = c["id"]
                url = c.get("url", "")
                m = re.search(r'#issuecomment-(\d+)', url)
                if m:
                    existing_comment_db_id = m.group(1)
                break
                
    with open("temp_comment.md", "w") as tf:
        tf.write(body)
        
    if existing_comment_db_id:
        print(f"Found existing comment with DB ID {existing_comment_db_id}. Editing via gh issue comment...")
        # Since 'gh issue comment' command can edit using the URL!
        comment_url = f"https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/{COORDINATOR_ISSUE}#issuecomment-{existing_comment_db_id}"
        run_cmd(["gh", "issue", "comment", comment_url, "-F", "temp_comment.md"])
        print("Comment edited successfully!")
    else:
        print("No existing comment found. Creating new comment...")
        run_cmd(["gh", "issue", "comment", COORDINATOR_ISSUE, "-F", "temp_comment.md"])
        print("Comment created successfully!")
        
    if os.path.exists("temp_comment.md"):
        os.remove("temp_comment.md")

if __name__ == "__main__":
    main()
