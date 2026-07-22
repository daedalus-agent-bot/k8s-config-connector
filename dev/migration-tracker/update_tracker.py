import json
import re
import os
import subprocess
import sys

def run_command(cmd, input_data=None):
    """Runs a shell command and returns stdout as string. Raises error on failure."""
    try:
        p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out, err = p.communicate(input=input_data)
        if p.returncode != 0:
            print(f"Command '{cmd}' failed with exit code {p.returncode}", file=sys.stderr)
            print(f"Stderr: {err}", file=sys.stderr)
            raise RuntimeError(f"Command failed: {err}")
        return out.strip()
    except Exception as e:
        print(f"Error executing command '{cmd}': {e}", file=sys.stderr)
        raise

def parse_static_config(file_path):
    """Parses static_config.go and returns a set of (group, kind) that support Direct reconciler."""
    pattern = re.compile(r'Group:\s*"([^"]+)",\s*Kind:\s*"([^"]+)"\s*}:\s*{(.*?)}')
    registered_direct = set()
    if not os.path.exists(file_path):
        print(f"Error: static_config.go not found at {file_path}", file=sys.stderr)
        return registered_direct
    
    with open(file_path, "r") as f:
        content = f.read()
    
    for match in pattern.finditer(content):
        group_full = match.group(1)
        kind = match.group(2)
        config_body = match.group(3)
        if "ReconcilerTypeDirect" in config_body:
            # Group is like "alloydb.cnrm.cloud.google.com" or "apigateway.cnrm.cloud.google.com"
            # In data.json, group is "alloydb", "apigateway", etc.
            # So extract the prefix before the first dot.
            group_prefix = group_full.split(".")[0]
            registered_direct.add((group_prefix, kind))
            
    return registered_direct

def check_stage5(service, version, kind):
    paths = [
        f"pkg/controller/direct/{service}/{kind.lower()}_controller.go",
        f"pkg/controller/direct/{service}/{kind}_controller.go",
        f"pkg/controller/direct/{service}/adapter.go",
    ]
    for p in paths:
        if os.path.exists(p):
            return True
    return False

def check_stage4(service, version, kind):
    if os.path.exists(f"mockgcp/mock{service}") or os.path.exists(f"mockgcp/mock{service.lower()}"):
        return True
    
    dir_direct = f"pkg/controller/direct/{service}"
    if os.path.exists(dir_direct):
        for f in os.listdir(dir_direct):
            if f.endswith("_test.go") or "test" in f.lower():
                return True
                
    test_paths = [
        f"pkg/test/resourcefixture/testdata/basic/{service}/{version}/{kind}",
        f"pkg/test/resourcefixture/testdata/basic/{service}/{version}/{kind.lower()}",
        f"pkg/test/resourcefixture/testdata/basic/{service}/{kind}",
        f"pkg/test/resourcefixture/testdata/basic/{service}/{kind.lower()}",
    ]
    for p in test_paths:
        if os.path.exists(p):
            return True
    return False

def check_stage3(service, version, kind):
    paths = [
        f"pkg/controller/direct/{service}/{kind.lower()}_fuzzer.go",
        f"pkg/controller/direct/{service}/{kind}_fuzzer.go",
    ]
    for p in paths:
        if os.path.exists(p):
            return True
    return False

def check_stage2(service, version, kind):
    paths = [
        f"apis/{service}/{version}/{kind.lower()}_identity.go",
        f"apis/{service}/{version}/{kind}_identity.go",
        f"apis/{service}/{version}/{kind.lower()}_reference.go",
        f"apis/{service}/{version}/{kind}_reference.go",
    ]
    for p in paths:
        if os.path.exists(p):
            return True
    return False

def check_stage1(service, version, kind):
    paths = [
        f"apis/{service}/{version}/{kind.lower()}_types.go",
        f"apis/{service}/{version}/{kind}_types.go",
    ]
    for p in paths:
        if os.path.exists(p):
            return True
    return False

def infer_stage_from_pr_issue(title, body):
    text = (title + " " + body).lower()
    if "controller" in text or "adapter" in text or "reconcile" in text or "reconciliation" in text or "stage 5" in text:
        return "Stage 5 (Controller Implemented)"
    if "mockgcp" in text or "fixture" in text or "test" in text or "stage 4" in text:
        return "Stage 4 (MockGCP/E2E Fixtures)"
    if "fuzzer" in text or "mapper" in text or "stage 3" in text:
        return "Stage 3 (KRM Fuzzer)"
    if "identity" in text or "reference" in text or "stage 2" in text:
        return "Stage 2 (Identity & Reference Types)"
    if "type" in text or "crd" in text or "generate.sh" in text or "stage 1" in text:
        return "Stage 1 (Direct KRM Types)"
    return "Investigation/Setup"

def match_kind(kind, text):
    pattern = r'\b' + re.escape(kind.lower()) + r'\b'
    return bool(re.search(pattern, text.lower()))

def main():
    print("--- Starting update_tracker.py ---")
    
    # Paths
    static_config_path = "pkg/controller/resourceconfig/static_config.go"
    tracker_data_path = "dev/migration-tracker/data.json"
    
    # 1. Parse static_config.go
    print(f"Parsing {static_config_path}...")
    registered_direct = parse_static_config(static_config_path)
    print(f"Found {len(registered_direct)} registered direct controllers in static_config.go.")
    
    # 2. Load dev/migration-tracker/data.json
    print(f"Loading {tracker_data_path}...")
    with open(tracker_data_path, "r") as f:
        data = json.load(f)
    print(f"Loaded {len(data)} resources from migration tracker data.")
    
    # 3. Retrieve GitHub Data
    print("Retrieving migration issues (SET 1) from GitHub...")
    # Labeled "overseer" and "workflow/migrate"
    issues_set1_raw = run_command('gh issue list --state all --label "overseer","workflow/migrate" --json number,title,labels,assignees,createdAt,state,url --limit 1000')
    issues_set1 = json.loads(issues_set1_raw)
    print(f"Found {len(issues_set1)} migration issues.")
    
    print("Retrieving all open issues (SET 2) from GitHub...")
    open_issues_raw = run_command('gh issue list --state open --limit 2000 --json number,title,url,assignees,author,state,body')
    open_issues = json.loads(open_issues_raw)
    print(f"Found {len(open_issues)} open issues.")
    
    print("Retrieving all open PRs (SET 2) from GitHub...")
    open_prs_raw = run_command('gh pr list --state open --limit 1000 --json number,title,url,author,state,body')
    open_prs = json.loads(open_prs_raw)
    print(f"Found {len(open_prs)} open PRs.")
    
    # Combine open issues and PRs for external searching & stage inference
    all_open_items = open_issues + open_prs
    
    # Helpers for tracking issue matching
    kind_to_migration_issues = {}
    for issue in issues_set1:
        title = issue.get("title", "")
        # Find which Kinds this overseer issue might refer to
        # Let's check each resource in tracker
        for r in data:
            r_kind = r["kind"]
            if match_kind(r_kind, title):
                if r_kind not in kind_to_migration_issues:
                    kind_to_migration_issues[r_kind] = []
                kind_to_migration_issues[r_kind].append(issue)
                
    # 4. Audit & Update each resource block
    print("Auditing each resource...")
    for r in data:
        group = r["group"]
        kind = r["kind"]
        version = r["version"]
        
        is_direct_in_code = (group, kind) in registered_direct
        
        # Check files on disk to find the max stage
        stage5_exists = check_stage5(group, version, kind)
        stage4_exists = check_stage4(group, version, kind)
        stage3_exists = check_stage3(group, version, kind)
        stage2_exists = check_stage2(group, version, kind)
        stage1_exists = check_stage1(group, version, kind)
        
        has_any_files = stage5_exists or stage4_exists or stage3_exists or stage2_exists or stage1_exists
        
        if is_direct_in_code:
            # Case A: Registered in static_config.go
            r["state"] = "Completed"
            r["steps"] = {
                "gen-types": True,
                "identity-reference": True,
                "mapper-fuzzer": True,
                "mocks": True,
                "controller": True,
                "tests": True
            }
            r["stage"] = "Stage 5 (Controller Implemented)"
            r["trackingIssue"] = ""
            r["assignee"] = ""
        else:
            # Case B: NOT registered in static_config.go
            # First, check if there are migration tracking issues (SET 1)
            mig_issues = kind_to_migration_issues.get(kind, [])
            
            open_mig_issues = [i for i in mig_issues if i["state"].upper() == "OPEN"]
            closed_mig_issues = [i for i in mig_issues if i["state"].upper() == "CLOSED"]
            
            has_open_mig = len(open_mig_issues) > 0
            has_closed_mig = len(closed_mig_issues) > 0
            
            # Revert from completed if it was marked as completed
            if r["state"] == "Completed":
                if has_any_files or has_open_mig or has_closed_mig:
                    r["state"] = "In Progress"
                else:
                    r["state"] = "Not Started"
            
            # Determine stage
            determined_stage = "Investigation/Setup"
            if stage5_exists:
                determined_stage = "Stage 5 (Controller Implemented)"
            elif stage4_exists:
                determined_stage = "Stage 4 (MockGCP/E2E Fixtures)"
            elif stage3_exists:
                determined_stage = "Stage 3 (KRM Fuzzer)"
            elif stage2_exists:
                determined_stage = "Stage 2 (Identity & Reference Types)"
            elif stage1_exists:
                determined_stage = "Stage 1 (Direct KRM Types)"
            else:
                # Infer stage from open PRs/issues
                for item in all_open_items:
                    if match_kind(kind, item.get("title", "")):
                        determined_stage = infer_stage_from_pr_issue(item.get("title", ""), item.get("body", "") or "")
                        break
            
            r["stage"] = determined_stage
            
            # Handle tracking issue
            if has_open_mig:
                # Take the first open tracking issue
                primary_issue = open_mig_issues[0]
                r["state"] = "In Progress"
                r["trackingIssue"] = primary_issue["url"]
                # assignee login
                assignees = primary_issue.get("assignees", [])
                if assignees:
                    r["assignee"] = assignees[0].get("login", "")
                else:
                    r["assignee"] = ""
            else:
                # No open migration issues
                r["trackingIssue"] = ""
                r["assignee"] = ""
                
                # Check closed migration issues for anomaly notes
                if has_closed_mig:
                    closed_issue = closed_mig_issues[0]
                    num = closed_issue["number"]
                    r["notes"] = f"Tracking issue #{num} is closed but direct controller is not registered in code"
                    if has_any_files:
                        r["state"] = "In Progress"
                    else:
                        r["state"] = "Not Started"
                else:
                    # Clean notes of closed tracking issue anomaly if it doesn't exist anymore
                    if "closed but direct controller is not registered" in r.get("notes", ""):
                        r["notes"] = ""
            
            # If no tracking issue but has files or external work, ensure state is "In Progress"
            if r["state"] != "In Progress" and has_any_files:
                r["state"] = "In Progress"
                
            # Now, scan for other/external issues and PRs (SET 2)
            # Find open issues/PRs containing the Kind name that are NOT the tracking issue,
            # and NOT created by bot accounts.
            external_refs = []
            for item in all_open_items:
                title = item.get("title", "")
                num = item.get("number")
                url = item.get("url", "")
                author = item.get("author", {}).get("login", "")
                
                # Filter bots
                if "bot" in author.lower() or "robot" in author.lower():
                    continue
                
                # Skip if it is the primary tracking issue
                if r["trackingIssue"] == url:
                    continue
                
                if match_kind(kind, title):
                    external_refs.append(num)
            
            if external_refs:
                # We have active external work!
                r["state"] = "In Progress"
                # Record in notes
                # Remove existing "External Work: ..." from notes to avoid accumulation, then add new ones
                current_notes = r.get("notes", "") or ""
                # Filter out old External Work notes
                notes_parts = [p.strip() for p in current_notes.split(",") if p.strip()]
                notes_parts = [p for p in notes_parts if not p.startswith("External Work:")]
                
                for ref in sorted(list(set(external_refs))):
                    notes_parts.append(f"External Work: #{ref}")
                
                r["notes"] = ", ".join(notes_parts)
            else:
                # No new external work found, but preserve existing notes if they are not external work
                current_notes = r.get("notes", "") or ""
                notes_parts = [p.strip() for p in current_notes.split(",") if p.strip()]
                notes_parts = [p for p in notes_parts if not p.startswith("External Work:")]
                r["notes"] = ", ".join(notes_parts)

    # 5. Save updated dev/migration-tracker/data.json
    print(f"Saving updated {tracker_data_path}...")
    with open(tracker_data_path, "w") as f:
        json.dump(data, f, indent=2)
    print("Local tracking data successfully updated.")
    
    # 6. Count totals
    completed_count = sum(1 for r in data if r["state"] == "Completed")
    in_progress_count = sum(1 for r in data if r["state"] == "In Progress")
    pending_count = 0
    total_count = len(data)
    
    completed_kinds = {r["kind"] for r in data if r["state"] == "Completed"}
    
    next_resources = []
    for r in data:
        if r["state"] == "Not Started" and r["defaultController"] in ["Terraform", "DCL"]:
            # Check dependencies
            deps = r.get("dependencies", [])
            all_deps_completed = True
            for d in deps:
                if d not in completed_kinds:
                    all_deps_completed = False
                    break
            if all_deps_completed:
                next_resources.append(r)
                
    pending_count = len(next_resources)
    # Sort next resources by sortOrder ascending
    next_resources.sort(key=lambda x: x["sortOrder"])
    
    print(f"High-level Status:")
    print(f"  Completed: {completed_count}")
    print(f"  In Progress: {in_progress_count}")
    print(f"  Pending: {pending_count}")
    print(f"  Total: {total_count}")
    
    # 7. Construct summary markdown
    summary_md = []
    summary_md.append("### Migration Progress Tracker Summary\n")
    summary_md.append("## High-Level Status")
    summary_md.append("| State | Count |")
    summary_md.append("|-------|-------|")
    summary_md.append(f"| Completed | {completed_count} |")
    summary_md.append(f"| In Progress | {in_progress_count} |")
    summary_md.append(f"| Pending | {pending_count} |")
    summary_md.append(f"| Total | {total_count} |\n")
    
    summary_md.append("## In Progress Resources")
    summary_md.append("| Kind | Current Stage | Tracking Issue/PR | Assignee | Notes |")
    summary_md.append("|------|---------------|-------------------|----------|-------|")
    
    in_progress_resources = [r for r in data if r["state"] == "In Progress"]
    in_progress_resources.sort(key=lambda x: x["kind"])
    for r in in_progress_resources:
        kind = r["kind"]
        stage = r["stage"]
        tracking_issue = r["trackingIssue"]
        assignee = r["assignee"]
        notes = r.get("notes", "") or ""
        
        if tracking_issue:
            # Extract issue number from URL
            issue_num = tracking_issue.split("/")[-1]
            tracking_str = f"[#{issue_num}]({tracking_issue})"
        else:
            tracking_str = "N/A"
            
        summary_md.append(f"| {kind} | {stage} | {tracking_str} | {assignee} | {notes} |")
        
    summary_md.append("\n## Next Resources (Pending & Unblocked)")
    summary_md.append("| Kind | Sort Order | Default Controller | Dependencies | Notes |")
    summary_md.append("|------|------------|--------------------|--------------|-------|")
    for r in next_resources:
        kind = r["kind"]
        sort_order = r["sortOrder"]
        controller = r["defaultController"]
        deps = ", ".join(r.get("dependencies", []))
        notes = r.get("notes", "") or ""
        summary_md.append(f"| {kind} | {sort_order} | {controller} | {deps} | {notes} |")
        
    summary_md.append("\n## Completed Resources")
    summary_md.append("| Kind | Default Controller | Date Completed / Notes |")
    summary_md.append("|------|--------------------|------------------------|")
    completed_resources = [r for r in data if r["state"] == "Completed"]
    completed_resources.sort(key=lambda x: x["kind"])
    for r in completed_resources:
        kind = r["kind"]
        controller = r["defaultController"]
        summary_md.append(f"| {kind} | {controller} | Registered in code |")
        
    summary_body = "\n".join(summary_md)
    
    # 8. Update Coordinator Issue Comment
    coordinator_issue_num = "10588"
    print(f"Finding existing summary comment on coordinator issue #{coordinator_issue_num}...")
    
    # List comments via gh api
    comments_raw = run_command(f"gh api repos/GoogleCloudPlatform/k8s-config-connector/issues/{coordinator_issue_num}/comments --paginate")
    comments = json.loads(comments_raw)
    
    existing_comment_id = None
    for comment in comments:
        body = comment.get("body", "") or ""
        if "### Migration Progress Tracker Summary" in body:
            existing_comment_id = comment.get("id")
            break
            
    if existing_comment_id:
        print(f"Found existing comment ID: {existing_comment_id}. Editing...")
        # Write body to a temp file to avoid shell expansion / argument length limit issues
        temp_body_path = "dev/migration-tracker/temp_summary.md"
        with open(temp_body_path, "w") as f_temp:
            f_temp.write(summary_body)
            
        # Run gh command to edit the comment
        run_command(f'gh api -X PATCH repos/GoogleCloudPlatform/k8s-config-connector/issues/comments/{existing_comment_id} -F body=@{temp_body_path}')
        os.remove(temp_body_path)
        print("Comment updated successfully.")
    else:
        print("No existing summary comment found. Creating a new one...")
        temp_body_path = "dev/migration-tracker/temp_summary.md"
        with open(temp_body_path, "w") as f_temp:
            f_temp.write(summary_body)
            
        run_command(f'gh api repos/GoogleCloudPlatform/k8s-config-connector/issues/{coordinator_issue_num}/comments -F body=@{temp_body_path}')
        os.remove(temp_body_path)
        print("Comment created successfully.")

if __name__ == "__main__":
    main()
