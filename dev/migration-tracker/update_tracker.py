#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys

COORDINATOR_ISSUE_NUMBER = 10588

def run_command(args):
    print(f"Running command: {' '.join(args)}")
    result = subprocess.run(args, capture_output=True, text=True, check=True)
    return result.stdout.strip()

def is_bot(username):
    if not username:
        return False
    u = username.lower()
    return "bot" in u or "robot" in u

def parse_registered_direct_kinds(static_config_path):
    registered_kinds = set()
    if not os.path.exists(static_config_path):
        return registered_kinds
    with open(static_config_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    for line in content.splitlines():
        if "Kind:" in line:
            match = re.search(r'Kind:\s*"([^"]+)"', line)
            if match:
                kind = match.group(1)
                if "k8s.ReconcilerTypeDirect" in line:
                    registered_kinds.add(kind)
    return registered_kinds

def has_types_go(group, version, kind):
    # Check apis/{group}/{version} or apis/{group}
    dir_path = f"apis/{group}/{version}"
    if not os.path.exists(dir_path):
        dir_path = f"apis/{group}"
        if not os.path.exists(dir_path):
            return False
            
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".go") and not file.endswith("_test.go"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        if f"type {kind} struct" in f.read():
                            return True
                except Exception:
                    pass
    return False

def has_identity_ref_go(group, version, kind):
    dir_path = f"apis/{group}/{version}"
    if not os.path.exists(dir_path):
        dir_path = f"apis/{group}"
        if not os.path.exists(dir_path):
            return False
            
    low_kind = kind.lower()
    low_kind_stripped = kind.replace(group, "").lower() if kind.lower().startswith(group.lower()) else low_kind
    
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith("_identity.go") or file.endswith("_reference.go"):
                if low_kind in file.lower() or low_kind_stripped in file.lower():
                    return True
                
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        if kind in f.read():
                            return True
                except Exception:
                    pass
    return False

def has_fuzzer_go(group, kind):
    dir_path = f"pkg/controller/direct/{group}"
    if not os.path.exists(dir_path):
        return False
        
    low_kind = kind.lower()
    low_kind_stripped = kind.replace(group, "").lower() if kind.lower().startswith(group.lower()) else low_kind
    
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith("_fuzzer.go"):
                if low_kind in file.lower() or low_kind_stripped in file.lower():
                    return True
                
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        if kind in f.read():
                            return True
                except Exception:
                    pass
    return False

def has_mocks_or_fixtures(group, version, kind):
    low_kind = kind.lower()
    fixture_dir = f"pkg/test/resourcefixture/testdata/basic/{group}/{version}/{low_kind}"
    if os.path.exists(fixture_dir):
        return True
    fixture_dir_no_ver = f"pkg/test/resourcefixture/testdata/basic/{group}/{low_kind}"
    if os.path.exists(fixture_dir_no_ver):
        return True
        
    basic_dir = "pkg/test/resourcefixture/testdata/basic"
    if os.path.exists(basic_dir):
        for root, dirs, _ in os.walk(basic_dir):
            for d in dirs:
                if d == low_kind and group in root:
                    return True

    if os.path.exists(f"mockgcp/mock{group}"):
        return True
        
    direct_test_dir = f"pkg/controller/direct/{group}"
    if os.path.exists(direct_test_dir):
        for root, _, files in os.walk(direct_test_dir):
            for file in files:
                if file.endswith("_test.go"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            if kind in f.read():
                                return True
                    except Exception:
                        pass
    return False

def has_controller_go(group, kind):
    dir_path = f"pkg/controller/direct/{group}"
    if not os.path.exists(dir_path):
        return False
        
    low_kind = kind.lower()
    low_kind_stripped = kind.replace(group, "").lower() if kind.lower().startswith(group.lower()) else low_kind
    
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith("_controller.go") or file == "adapter.go":
                if low_kind in file.lower() or low_kind_stripped in file.lower():
                    return True
                if file == "adapter.go":
                    return True
                
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        if kind in content or "RegisterModel" in content:
                            return True
                except Exception:
                    pass
    return False

def rebuild_notes(kind, existing_notes, closed_anomaly, external_works):
    parts = []
    if existing_notes:
        for p in existing_notes.split(","):
            p_strip = p.strip()
            if not p_strip:
                continue
            # Filter out automated elements
            if p_strip.startswith("External Work:") or ("is closed but direct controller is not registered in code" in p_strip):
                continue
            parts.append(p_strip)
            
    if closed_anomaly:
        parts.append(closed_anomaly)
        
    for ew in sorted(list(set(external_works))):
        parts.append(f"External Work: #{ew}")
        
    return ", ".join(parts)

def main():
    data_path = "dev/migration-tracker/data.json"
    static_config_path = "pkg/controller/resourceconfig/static_config.go"
    
    if not os.path.exists(data_path):
        print(f"Error: tracking file {data_path} not found.")
        sys.exit(1)
        
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    # Step 2: Audit Ground Reality in Code
    registered_kinds = parse_registered_direct_kinds(static_config_path)
    print(f"Registered Direct Kinds in static_config.go ({len(registered_kinds)}): {sorted(list(registered_kinds))}")
    
    # Pre-build mappings and check if direct controllers are registered
    all_kinds = [d["kind"] for d in data]
    kind_to_data = {d["kind"]: d for d in data}
    
    for d in data:
        kind = d["kind"]
        if kind in registered_kinds:
            d["state"] = "Completed"
            d["stage"] = "Stage 5 (Controller Implemented)"
            if "steps" not in d:
                d["steps"] = {}
            for step in ["gen-types", "identity-reference", "mapper-fuzzer", "mocks", "controller", "tests"]:
                d["steps"][step] = True
        else:
            # If not registered, ensure state is not Completed
            if d.get("state") == "Completed":
                d["state"] = "In Progress"
                
    # Step 3: Scan GitHub for Active and External Work (SET 1)
    issues_json = run_command(["gh", "issue", "list", "--state", "all", "--label", "overseer,workflow/migrate", "--limit", "1000", "--json", "number,title,labels,assignees,createdAt,state,url"])
    overseer_issues = json.loads(issues_json)
    print(f"Fetched {len(overseer_issues)} migration overseer issues/PRs.")
    
    # Group issues by Kind
    kind_to_overseer_issues = {}
    for issue in overseer_issues:
        title = issue.get("title", "")
        # Exclude tracker itself
        if issue.get("number") == COORDINATOR_ISSUE_NUMBER:
            continue
        for kind in all_kinds:
            if re.search(r'\b' + re.escape(kind) + r'\b', title):
                kind_to_overseer_issues.setdefault(kind, []).append(issue)
                break # Matched this issue to this Kind, stop checking others
                
    # Map from issue URL to Kind to avoid counting tracking issue as external work
    tracked_issue_urls = set()
    closed_anomalies = {}
    
    for kind, issues in kind_to_overseer_issues.items():
        d = kind_to_data[kind]
        # Sort issues so open ones come first
        open_issues = [i for i in issues if i.get("state") == "OPEN"]
        closed_issues = [i for i in issues if i.get("state") != "OPEN"]
        
        if kind in registered_kinds:
            # Already completed, we don't need active tracking issues
            d["trackingIssue"] = ""
            d["assignee"] = ""
            continue
            
        if open_issues:
            # Use the first open issue as tracking
            issue = open_issues[0]
            d["state"] = "In Progress"
            d["trackingIssue"] = issue.get("url", "")
            tracked_issue_urls.add(issue.get("url", ""))
            
            # Extract assignee
            assignees = issue.get("assignees", [])
            if assignees:
                d["assignee"] = assignees[0].get("login", "")
            else:
                d["assignee"] = ""
        else:
            # Only closed issues found and not registered in code (anomaly!)
            d["trackingIssue"] = ""
            d["assignee"] = ""
            if closed_issues:
                issue = closed_issues[0]
                closed_anomalies[kind] = f"Tracking issue #{issue.get('number')} is closed but direct controller is not registered in code"
                
    # Scan GitHub for Other/External Issues and PRs (SET 2)
    open_issues_json = run_command(["gh", "issue", "list", "--state", "open", "--limit", "1000", "--json", "number,title,url,author"])
    open_prs_json = run_command(["gh", "pr", "list", "--state", "open", "--limit", "1000", "--json", "number,title,url,author"])
    
    open_issues = json.loads(open_issues_json)
    open_prs = json.loads(open_prs_json)
    
    print(f"Fetched {len(open_issues)} open issues and {len(open_prs)} open PRs.")
    
    external_work_by_kind = {}
    
    for item in open_issues + open_prs:
        title = item.get("title", "")
        url = item.get("url", "")
        author_login = item.get("author", {}).get("login", "") if item.get("author") else ""
        number = item.get("number")
        
        if number == COORDINATOR_ISSUE_NUMBER:
            continue
        if is_bot(author_login):
            continue
        if url in tracked_issue_urls:
            continue
            
        # Check if any uncompleted Kind name is in the title
        for kind in all_kinds:
            d = kind_to_data[kind]
            if d.get("state") != "Completed":
                # Exact word-boundary match for Kind
                if re.search(r'\b' + re.escape(kind) + r'\b', title):
                    external_work_by_kind.setdefault(kind, []).append(number)
                    d["state"] = "In Progress"
                    break
                    
    # Step 4: Determine Current Stage for In Progress Resources
    for d in data:
        kind = d["kind"]
        group = d["group"]
        version = d.get("version", "v1beta1")
        
        # Build anomaly & external notes
        closed_anomaly = closed_anomalies.get(kind, "")
        ext_works = external_work_by_kind.get(kind, [])
        d["notes"] = rebuild_notes(kind, d.get("notes", ""), closed_anomaly, ext_works)
        
        if d.get("state") == "Completed":
            d["stage"] = "Stage 5 (Controller Implemented)"
            continue
            
        # File checks
        s5 = has_controller_go(group, kind)
        s4 = has_mocks_or_fixtures(group, version, kind)
        s3 = has_fuzzer_go(group, kind)
        s2 = has_identity_ref_go(group, version, kind)
        s1 = has_types_go(group, version, kind)
        
        # Populate steps based on actual filesystem status for accuracy
        if "steps" not in d:
            d["steps"] = {}
        d["steps"]["gen-types"] = s1 or s2 or s3 or s4 or s5
        d["steps"]["identity-reference"] = s2 or s3 or s4 or s5
        d["steps"]["mapper-fuzzer"] = s3 or s4 or s5
        d["steps"]["mocks"] = s4 or s5
        d["steps"]["controller"] = s5
        d["steps"]["tests"] = s4 or s5 # typically if mocks/fixtures are there, tests are there
        
        if s5:
            d["state"] = "In Progress"
            d["stage"] = "Stage 5 (Controller Implemented)"
        elif s4:
            d["state"] = "In Progress"
            d["stage"] = "Stage 4 (MockGCP/E2E Fixtures)"
        elif s3:
            d["state"] = "In Progress"
            d["stage"] = "Stage 3 (KRM Fuzzer)"
        elif s2:
            d["state"] = "In Progress"
            d["stage"] = "Stage 2 (Identity & Reference Types)"
        elif s1:
            d["state"] = "In Progress"
            d["stage"] = "Stage 1 (Direct KRM Types)"
        else:
            d["stage"] = "Investigation/Setup"
            # If no files exist, and there is no active tracking issue or external work, revert to Not Started
            has_active_work = bool(d.get("trackingIssue")) or bool(ext_works)
            if not has_active_work:
                d["state"] = "Not Started"
                
    # Step 5: Identify Next Pending Resources
    completed_kinds = set(d["kind"] for d in data if d.get("state") == "Completed")
    
    pending_unblocked = []
    for d in data:
        if d.get("state") == "Not Started":
            if d.get("defaultController") in ["Terraform", "DCL"]:
                deps = d.get("dependencies", [])
                if all(dep in completed_kinds for dep in deps):
                    pending_unblocked.append(d)
                    
    pending_unblocked.sort(key=lambda x: x.get("sortOrder", 999))
    
    # Step 6: Save Local Tracking Data
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Successfully saved updated local tracking data to {data_path}.")
    
    # Step 7: Construct Progress Summary Comment
    completed_count = sum(1 for d in data if d.get("state") == "Completed")
    in_progress_count = sum(1 for d in data if d.get("state") == "In Progress")
    pending_count = sum(1 for d in data if d.get("state") == "Not Started")
    total_count = len(data)
    
    # In Progress Resources Table
    in_progress_rows = []
    in_progress_data = [d for d in data if d.get("state") == "In Progress"]
    in_progress_data.sort(key=lambda x: x["kind"])
    
    for d in in_progress_data:
        kind = d["kind"]
        stage = d.get("stage", "Investigation/Setup")
        ti_url = d.get("trackingIssue", "")
        if ti_url:
            # Extract issue number from URL
            m = re.search(r'/issues/(\d+)', ti_url)
            num = m.group(1) if m else "Link"
            ti_str = f"[#{num}]({ti_url})"
        else:
            ti_str = "N/A"
        assignee = d.get("assignee", "")
        notes = d.get("notes", "")
        in_progress_rows.append(f"| {kind} | {stage} | {ti_str} | {assignee} | {notes} |")
        
    # Pending/Unblocked Resources Table
    pending_rows = []
    for d in pending_unblocked:
        kind = d["kind"]
        so = d.get("sortOrder", "")
        ctrl = d.get("defaultController", "")
        deps = ", ".join(d.get("dependencies", []))
        notes = d.get("notes", "")
        pending_rows.append(f"| {kind} | {so} | {ctrl} | {deps} | {notes} |")
        
    # Completed Resources Table
    completed_rows = []
    completed_data = [d for d in data if d.get("state") == "Completed"]
    completed_data.sort(key=lambda x: x["kind"])
    for d in completed_data:
        kind = d["kind"]
        ctrl = d.get("defaultController", "")
        notes = d.get("notes", "")
        if not notes:
            notes = "Registered in code"
        completed_rows.append(f"| {kind} | {ctrl} | {notes} |")
        
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
""" + "\n".join(pending_rows) + """

## Completed Resources
| Kind | Default Controller | Date Completed / Notes |
|------|--------------------|------------------------|
""" + "\n".join(completed_rows) + "\n"

    # Write summary body to a temp file for safety with gh cli
    with open("summary_comment.md", "w", encoding="utf-8") as f:
        f.write(summary_body)
        
    # Find existing comments to see if we should edit or create
    comments_json = run_command(["gh", "api", f"repos/GoogleCloudPlatform/k8s-config-connector/issues/{COORDINATOR_ISSUE_NUMBER}/comments"])
    comments = json.loads(comments_json)
    
    target_comment_id = None
    for comment in comments:
        if "### Migration Progress Tracker Summary" in comment.get("body", ""):
            target_comment_id = comment.get("id")
            break
            
    if target_comment_id:
        print(f"Found existing tracker summary comment with ID: {target_comment_id}. Editing it...")
        run_command(["gh", "api", "-X", "PATCH", f"repos/GoogleCloudPlatform/k8s-config-connector/issues/comments/{target_comment_id}", "-F", "body=@summary_comment.md"])
    else:
        print(f"No existing comment found. Creating a new tracker summary comment on issue {COORDINATOR_ISSUE_NUMBER}...")
        run_command(["gh", "issue", "comment", str(COORDINATOR_ISSUE_NUMBER), "--body-file", "summary_comment.md"])
        
    # Cleanup temp file
    if os.path.exists("summary_comment.md"):
        os.remove("summary_comment.md")
        
    print("Done!")

if __name__ == "__main__":
    main()
