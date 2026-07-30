#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys

def main():
    # 1. Parse static_config.go to find registered direct controllers
    print("Parsing static_config.go...")
    registered_kinds = set()
    with open("pkg/controller/resourceconfig/static_config.go", "r") as f:
        for line in f:
            m = re.search(r'Kind:\s*"([^"]+)"', line)
            if m:
                kind = m.group(1)
                if "k8s.ReconcilerTypeDirect" in line:
                    registered_kinds.add(kind)
    print(f"Found {len(registered_kinds)} registered direct controller Kinds.")

    # 2. Load dev/migration-tracker/data.json
    print("Loading data.json...")
    with open("dev/migration-tracker/data.json", "r") as f:
        data = json.load(f)

    # All known kinds in data.json
    all_tracker_kinds = set(item["kind"] for item in data)

    # 3. Fetch SET 1: Overseer/workflow migration issues (open and closed)
    print("Fetching active overseer/migrate issues from GitHub...")
    # Run gh command to fetch all issues
    res1 = subprocess.run([
        "gh", "issue", "list", "--state", "all",
        "--label", "overseer,workflow/migrate",
        "--json", "number,title,labels,assignees,state,url",
        "--limit", "1000"
    ], capture_output=True, text=True)
    if res1.returncode != 0:
        print("Error fetching overseer issues:", res1.stderr)
        sys.exit(1)
    overseer_issues = json.loads(res1.stdout)
    print(f"Fetched {len(overseer_issues)} overseer issues.")

    # Map overseer issues to Kinds
    overseer_by_kind = {}
    for issue in overseer_issues:
        title = issue["title"]
        matched_kind = None
        for k in all_tracker_kinds:
            if k.lower() in title.lower():
                if not matched_kind or len(k) > len(matched_kind):
                    matched_kind = k
        if matched_kind:
            if matched_kind not in overseer_by_kind:
                overseer_by_kind[matched_kind] = []
            overseer_by_kind[matched_kind].append(issue)

    # 4. Fetch SET 2: All open issues and PRs for external work matching Kind
    print("Fetching all open issues and PRs for external work...")
    res_issues = subprocess.run([
        "gh", "issue", "list", "--state", "open",
        "--limit", "2000",
        "--json", "number,title,body,url,assignees,author,state,labels"
    ], capture_output=True, text=True)
    if res_issues.returncode != 0:
        print("Error fetching open issues:", res_issues.stderr)
        sys.exit(1)
    open_issues = json.loads(res_issues.stdout)

    res_prs = subprocess.run([
        "gh", "pr", "list", "--state", "open",
        "--limit", "2000",
        "--json", "number,title,body,url,author,state,labels"
    ], capture_output=True, text=True)
    if res_prs.returncode != 0:
        print("Error fetching open PRs:", res_prs.stderr)
        sys.exit(1)
    open_prs = json.loads(res_prs.stdout)
    print(f"Fetched {len(open_issues)} open issues and {len(open_prs)} open PRs.")

    # Helper to check if user is bot/robot
    def is_bot(username):
        if not username:
            return False
        username_lower = username.lower()
        return "bot" in username_lower or "robot" in username_lower or "agent" in username_lower

    # Helper to clean up old notes
    def clean_notes(old_notes):
        if not old_notes:
            return ""
        parts = []
        for part in old_notes.split(", "):
            part = part.strip()
            if not part:
                continue
            if re.search(r'External Work:\s*#\d+', part):
                continue
            if re.search(r'Tracking issue\s*#\d+\s*is closed', part):
                continue
            if "Missing _reference.go or _identity.go" in part:
                continue
            parts.append(part)
        return ", ".join(parts)

    # Helper to determine stage from disk files
    def determine_stage_from_disk(group, version, kind):
        kind_lower = kind.lower()
        
        # Stage 5
        s5_files = [
            f"pkg/controller/direct/{group}/{kind_lower}_controller.go",
            f"pkg/controller/direct/{group}/adapter.go"
        ]
        if any(os.path.exists(f) for f in s5_files):
            return "Stage 5 (Controller Implemented)"
            
        # Stage 4
        s4_dirs = [
            f"mockgcp/mock{group}",
            f"pkg/test/resourcefixture/testdata/basic/{group}/{version}/{kind_lower}"
        ]
        if any(os.path.isdir(d) for d in s4_dirs):
            return "Stage 4 (MockGCP/E2E Fixtures)"
            
        # Stage 3
        s3_files = [
            f"pkg/controller/direct/{group}/{kind_lower}_fuzzer.go"
        ]
        if any(os.path.exists(f) for f in s3_files):
            return "Stage 3 (KRM Fuzzer)"
            
        # Stage 2
        s2_files = [
            f"apis/{group}/{version}/{kind_lower}_identity.go",
            f"apis/{group}/{version}/{kind_lower}_reference.go"
        ]
        if any(os.path.exists(f) for f in s2_files):
            return "Stage 2 (Identity & Reference Types)"
            
        # Stage 1
        s1_files = [
            f"apis/{group}/{version}/{kind_lower}_types.go"
        ]
        if any(os.path.exists(f) for f in s1_files):
            return "Stage 1 (Direct KRM Types)"
            
        return None

    # Process each resource in data.json
    completed_count = 0
    in_progress_count = 0
    not_started_count = 0

    print("Auditing ground reality and updating tracking data...")
    for item in data:
        kind = item["kind"]
        group = item["group"]
        version = item["version"]

        # Stage from disk
        disk_stage = determine_stage_from_disk(group, version, kind)

        # Check if direct controller is registered in static_config.go
        if kind in registered_kinds:
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
            item["assignee"] = ""
            item["trackingIssue"] = ""
            item["notes"] = ""
            completed_count += 1
            continue

        # If not registered in static_config.go
        if item["state"] == "Completed":
            if disk_stage:
                item["state"] = "In Progress"
            else:
                item["state"] = "Not Started"

        # Check tracking issues (SET 1)
        issues = overseer_by_kind.get(kind, [])
        open_tracker_issue = None
        closed_tracker_issue = None
        for issue in issues:
            if issue["state"] == "OPEN":
                open_tracker_issue = issue
                break
            elif issue["state"] == "CLOSED":
                closed_tracker_issue = issue

        item["trackingIssue"] = ""
        item["assignee"] = ""

        anomaly_note = ""
        if open_tracker_issue:
            item["state"] = "In Progress"
            item["trackingIssue"] = open_tracker_issue["url"]
            assignees = open_tracker_issue.get("assignees", [])
            if assignees:
                item["assignee"] = assignees[0]["login"]
        elif closed_tracker_issue:
            anomaly_note = f"Tracking issue #{closed_tracker_issue['number']} is closed but direct controller is not registered in code"

        # Determine Stage
        github_stage = None
        kind_open_issues = []
        kind_open_prs = []
        for issue in open_issues:
            if kind in issue["title"] or (issue["body"] and kind in issue["body"]):
                if not is_bot(issue["author"].get("login")):
                    if open_tracker_issue and issue["number"] == open_tracker_issue["number"]:
                        continue
                    if issue["number"] == 10588:
                        continue
                    kind_open_issues.append(issue)
        for pr in open_prs:
            if kind in pr["title"] or (pr["body"] and kind in pr["body"]):
                if not is_bot(pr["author"].get("login")):
                    kind_open_prs.append(pr)

        if not disk_stage:
            items_to_check = []
            if open_tracker_issue:
                items_to_check.append(open_tracker_issue)
            items_to_check.extend(kind_open_issues)
            items_to_check.extend(kind_open_prs)
            
            for git_item in items_to_check:
                labels = [l["name"] for l in git_item.get("labels", [])]
                if "step/controller" in labels or "step/tests" in labels:
                    github_stage = "Stage 5 (Controller Implemented)"
                    break
                elif "step/mockgcp" in labels:
                    github_stage = "Stage 4 (MockGCP/E2E Fixtures)"
                    break
                elif "step/mapper-fuzzer" in labels:
                    github_stage = "Stage 3 (KRM Fuzzer)"
                    break
                elif "step/identity-reference" in labels:
                    github_stage = "Stage 2 (Identity & Reference Types)"
                    break
                elif "step/gen-types" in labels:
                    github_stage = "Stage 1 (Direct KRM Types)"
                    break

            if github_stage:
                item["stage"] = github_stage
            else:
                item["stage"] = "Investigation/Setup"
        else:
            item["stage"] = disk_stage

        if disk_stage or open_tracker_issue or kind_open_issues or kind_open_prs:
            item["state"] = "In Progress"

        stage_num = 0
        if item["stage"].startswith("Stage 1"):
            stage_num = 1
        elif item["stage"].startswith("Stage 2"):
            stage_num = 2
        elif item["stage"].startswith("Stage 3"):
            stage_num = 3
        elif item["stage"].startswith("Stage 4"):
            stage_num = 4
        elif item["stage"].startswith("Stage 5"):
            stage_num = 5

        item["steps"] = {
            "gen-types": stage_num >= 1,
            "identity-reference": stage_num >= 2,
            "mapper-fuzzer": stage_num >= 3,
            "mocks": stage_num >= 4,
            "controller": stage_num >= 5,
            "tests": stage_num >= 5
        }

        # Handle notes
        base_notes = clean_notes(item.get("notes", ""))
        
        missing_ir = False
        if stage_num >= 4:
            kind_lower = kind.lower()
            id_path = f"apis/{group}/{version}/{kind_lower}_identity.go"
            ref_path = f"apis/{group}/{version}/{kind_lower}_reference.go"
            if not os.path.exists(id_path) or not os.path.exists(ref_path):
                missing_ir = True

        note_parts = []
        if base_notes:
            note_parts.append(base_notes)
        if missing_ir:
            note_parts.append("Missing _reference.go or _identity.go")
        if anomaly_note:
            note_parts.append(anomaly_note)

        external_work_ids = []
        for x in kind_open_issues:
            external_work_ids.append(x["number"])
        for x in kind_open_prs:
            external_work_ids.append(x["number"])
        external_work_ids = sorted(list(set(external_work_ids)))
        for ew_id in external_work_ids:
            note_parts.append(f"External Work: #{ew_id}")

        item["notes"] = ", ".join(note_parts)

        if item["state"] == "In Progress":
            in_progress_count += 1
        else:
            item["state"] = "Not Started"
            item["stage"] = "Investigation/Setup"
            not_started_count += 1

    print(f"Stats - Completed: {completed_count}, In Progress: {in_progress_count}, Not Started: {not_started_count}, Total: {len(data)}")

    # 5. Identify Next Pending Resources
    completed_kinds = set(item["kind"] for item in data if item["state"] == "Completed")
    pending_candidates = []
    for item in data:
        if item["state"] == "Not Started" and item["defaultController"] in ["Terraform", "DCL"]:
            deps = item.get("dependencies", [])
            all_deps_completed = True
            for dep in deps:
                if dep in all_tracker_kinds and dep not in completed_kinds:
                    all_deps_completed = False
                    break
            if all_deps_completed:
                pending_candidates.append(item)

    pending_candidates.sort(key=lambda x: x["sortOrder"])
    print(f"Found {len(pending_candidates)} pending unblocked candidates.")

    # Save dev/migration-tracker/data.json
    print("Saving updated data.json to disk...")
    with open("dev/migration-tracker/data.json", "w") as f:
        json.dump(data, f, indent=2)

    # 6. Generate Progress Summary comment body
    print("Constructing Progress Summary Comment...")
    
    total_count = len(data)
    pending_count = total_count - completed_count - in_progress_count

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
"""
    in_progress_items = [item for item in data if item["state"] == "In Progress"]
    in_progress_items.sort(key=lambda x: x["kind"])
    
    for item in in_progress_items:
        tracking_issue_formatted = "N/A"
        if item["trackingIssue"]:
            m = re.search(r'issues/(\d+)', item["trackingIssue"])
            if m:
                issue_num = m.group(1)
                tracking_issue_formatted = f"[#{issue_num}]({item['trackingIssue']})"
            else:
                tracking_issue_formatted = f"[Link]({item['trackingIssue']})"
        
        summary_body += f"| {item['kind']} | {item['stage']} | {tracking_issue_formatted} | {item['assignee']} | {item['notes']} |\n"

    summary_body += """
## Next Resources (Pending & Unblocked)
| Kind | Sort Order | Default Controller | Dependencies | Notes |
|------|------------|--------------------|--------------|-------|
"""
    for item in pending_candidates[:25]:
        deps_str = ", ".join(item.get("dependencies", []))
        summary_body += f"| {item['kind']} | {item['sortOrder']} | {item['defaultController']} | {deps_str} | {item['notes']} |\n"

    summary_body += """
## Completed Resources
| Kind | Default Controller | Date Completed / Notes |
|------|--------------------|------------------------|
"""
    completed_items = [item for item in data if item["state"] == "Completed"]
    completed_items.sort(key=lambda x: x["kind"])
    for item in completed_items:
        summary_body += f"| {item['kind']} | {item['defaultController']} | Registered in code |\n"

    comment_file = "dev/migration-tracker/comment_body.md"
    with open(comment_file, "w") as f:
        f.write(summary_body)
    print(f"Saved comment body to {comment_file}")

    # 7. Update coordinator issue comment
    coordinator_issue_num = "10588"
    print(f"Checking for existing tracker comments on issue #{coordinator_issue_num}...")
    
    res_comments = subprocess.run([
        "gh", "issue", "view", coordinator_issue_num, "--json", "comments"
    ], capture_output=True, text=True)
    if res_comments.returncode != 0:
        print("Error fetching issue comments:", res_comments.stderr)
        sys.exit(1)
    
    comments_data = json.loads(res_comments.stdout)
    existing_comment_id = None
    for comment in comments_data.get("comments", []):
        if "### Migration Progress Tracker Summary" in comment.get("body", ""):
            url = comment.get("url", "")
            m = re.search(r'#issuecomment-(\d+)', url)
            if m:
                existing_comment_id = m.group(1)
                print(f"Found existing comment ID: {existing_comment_id}")
                break

    if existing_comment_id:
        print(f"Editing existing comment #{existing_comment_id}...")
        res_edit = subprocess.run([
            "gh", "api", "-X", "PATCH",
            f"repos/GoogleCloudPlatform/k8s-config-connector/issues/comments/{existing_comment_id}",
            "-F", f"body=@{comment_file}"
        ], capture_output=True, text=True)
        if res_edit.returncode == 0:
            print("Successfully updated the coordinator issue comment!")
        else:
            print("Failed to update comment:", res_edit.stderr)
            sys.exit(1)
    else:
        print("Creating a new comment on coordinator issue...")
        res_create = subprocess.run([
            "gh", "api", "-X", "POST",
            f"repos/GoogleCloudPlatform/k8s-config-connector/issues/{coordinator_issue_num}/comments",
            "-F", f"body=@{comment_file}"
        ], capture_output=True, text=True)
        if res_create.returncode == 0:
            print("Successfully created a new coordinator issue comment!")
        else:
            print("Failed to create comment:", res_create.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
