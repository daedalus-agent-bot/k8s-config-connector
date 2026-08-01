import os
import json
import re
import subprocess

def get_all_files(root_dir):
    all_files = []
    if not os.path.exists(root_dir):
        return all_files
    for root, dirs, files in os.walk(root_dir):
        for f in files:
            all_files.append(os.path.join(root, f))
    return all_files

print("Starting tracking and audit run...")

# Initialize paths and file list caches
all_direct_files = get_all_files("pkg/controller/direct")
all_apis_files = get_all_files("apis")
all_fixture_files = get_all_files("pkg/test/resourcefixture/testdata/basic")

# Load data.json
data_path = "dev/migration-tracker/data.json"
with open(data_path, "r") as f:
    tracker_data = json.load(f)

# Step 2: Parse static_config.go
registered_kinds = set()
with open("pkg/controller/resourceconfig/static_config.go", "r") as f:
    for line in f:
        if "Group:" in line and "Kind:" in line:
            m_group = re.search(r'Group:\s*"([^"]+)"', line)
            m_kind = re.search(r'Kind:\s*"([^"]+)"', line)
            if m_group and m_kind:
                g = m_group.group(1)
                k = m_kind.group(1)
                m_supp = re.search(r'SupportedControllers:\s*\[\]k8s\.ReconcilerType\s*\{([^}]+)\}', line)
                if m_supp:
                    supp_controllers = m_supp.group(1)
                    if "ReconcilerTypeDirect" in supp_controllers or "Direct" in supp_controllers:
                        registered_kinds.add(k)

print(f"Registered kinds in static_config.go: {len(registered_kinds)}")

def matches_kind(filepath, group, kind):
    path_parts = [p.lower() for p in filepath.split(os.sep)]
    if group.lower() not in path_parts:
        return False
        
    filename = path_parts[-1].lower()
    k_lower = kind.lower()
    
    group_lower = group.lower()
    group_singular = group_lower[:-1] if group_lower.endswith('s') else group_lower
    
    stripped_kind = kind
    if k_lower.startswith(group_lower):
        stripped_kind = kind[len(group_lower):]
    elif k_lower.startswith(group_singular):
        stripped_kind = kind[len(group_singular):]
        
    sk_lower = stripped_kind.lower()
    
    if k_lower in filename or sk_lower in filename:
        return True
        
    if filename in ('adapter.go', 'controller.go', 'fuzzer.go'):
        if any(k_lower in p or sk_lower in p for p in path_parts[:-1]):
            return True
            
    return False

def determine_stages(group, kind, version):
    # Stage 5: Controller Implemented
    stage5 = False
    for f in all_direct_files:
        if matches_kind(f, group, kind):
            filename = os.path.basename(f).lower()
            if filename.endswith("_controller.go") or filename == "adapter.go":
                stage5 = True
                break
                
    # Stage 4: MockGCP / E2E Fixtures
    stage4 = False
    for f in all_direct_files:
        if matches_kind(f, group, kind):
            filename = os.path.basename(f).lower()
            if filename.endswith("_test.go"):
                stage4 = True
                break
    if not stage4:
        fixture_paths = [
            os.path.join("pkg/test/resourcefixture/testdata/basic", group.lower(), version.lower(), kind.lower()),
            os.path.join("pkg/test/resourcefixture/testdata/basic", group.lower(), kind.lower())
        ]
        for p in fixture_paths:
            if os.path.exists(p) and os.listdir(p):
                stage4 = True
                break
    if not stage4:
        mock_dir = os.path.join("mockgcp", f"mock{group.lower()}")
        if os.path.exists(mock_dir) and os.listdir(mock_dir):
            stage4 = True
            
    # Stage 3: KRM Fuzzer
    stage3 = False
    for f in all_direct_files:
        if matches_kind(f, group, kind):
            filename = os.path.basename(f).lower()
            if filename.endswith("_fuzzer.go"):
                stage3 = True
                break
                
    # Stage 2: Identity & Reference Types
    stage2 = False
    has_identity = False
    has_reference = False
    for f in all_apis_files:
        path_parts = [p.lower() for p in f.split(os.sep)]
        if group.lower() in path_parts and version.lower() in path_parts:
            if matches_kind(f, group, kind):
                filename = os.path.basename(f).lower()
                if filename.endswith("_identity.go"):
                    has_identity = True
                elif filename.endswith("_reference.go"):
                    has_reference = True
    if has_identity or has_reference:
        stage2 = True
        
    # Stage 1: Direct KRM Types
    stage1 = False
    for f in all_apis_files:
        path_parts = [p.lower() for p in f.split(os.sep)]
        if group.lower() in path_parts and version.lower() in path_parts:
            if matches_kind(f, group, kind):
                filename = os.path.basename(f).lower()
                if filename.endswith("_types.go"):
                    stage1 = True
                    break
                    
    steps = {
        "gen-types": stage1,
        "identity-reference": stage2,
        "mapper-fuzzer": stage3,
        "mocks": stage4,
        "controller": stage5,
        "tests": stage4
    }
    
    if stage5:
        return steps, "Stage 5 (Controller Implemented)"
    elif stage4:
        return steps, "Stage 4 (MockGCP/E2E Fixtures)"
    elif stage3:
        return steps, "Stage 3 (KRM Fuzzer)"
    elif stage2:
        return steps, "Stage 2 (Identity & Reference Types)"
    elif stage1:
        return steps, "Stage 1 (Direct KRM Types)"
    else:
        return steps, "Investigation/Setup"

# Step 3: Fetch active/external issues/PRs from GitHub
try:
    cmd_set1 = ["gh", "issue", "list", "--state", "all", "--label", "overseer,workflow/migrate", "--limit", "1000", "--json", "number,title,labels,assignees,createdAt,state,url"]
    res_set1 = subprocess.run(cmd_set1, capture_output=True, text=True, check=True)
    issues_set1 = json.loads(res_set1.stdout)
except Exception as e:
    print(f"Error fetching SET 1 issues: {e}")
    issues_set1 = []

try:
    cmd_set2_issues = ["gh", "issue", "list", "--state", "open", "--limit", "1000", "--json", "number,title,url,assignees,author,state"]
    res_set2_issues = subprocess.run(cmd_set2_issues, capture_output=True, text=True, check=True)
    open_issues = json.loads(res_set2_issues.stdout)
except Exception as e:
    print(f"Error fetching open issues: {e}")
    open_issues = []

try:
    cmd_set2_prs = ["gh", "pr", "list", "--state", "open", "--limit", "1000", "--json", "number,title,url,author,state"]
    res_set2_prs = subprocess.run(cmd_set2_prs, capture_output=True, text=True, check=True)
    open_prs = json.loads(res_set2_prs.stdout)
except Exception as e:
    print(f"Error fetching open PRs: {e}")
    open_prs = []

all_kinds_sorted = sorted([item["kind"] for item in tracker_data], key=len, reverse=True)

# Map overseer issues by kind
overseer_by_kind = {}
for issue in issues_set1:
    best_match = None
    for k in all_kinds_sorted:
        if k.lower() in issue["title"].lower():
            best_match = k
            break
    if best_match:
        if best_match not in overseer_by_kind:
            overseer_by_kind[best_match] = []
        overseer_by_kind[best_match].append(issue)

def get_external_work(open_items, kind, all_kinds_sorted, tracking_issue_num):
    matched_items = []
    for item in open_items:
        title = item["title"]
        num = item["number"]
        url = item["url"]
        
        best_match = None
        for k in all_kinds_sorted:
            if k.lower() in title.lower():
                best_match = k
                break
                
        if best_match == kind and num != tracking_issue_num:
            author_login = item.get("author", {}).get("login", "").lower() if item.get("author") else ""
            if "bot" in author_login or "robot" in author_login:
                continue
            matched_items.append(item)
    return matched_items

# Process all items
for resource in tracker_data:
    kind = resource["kind"]
    group = resource["group"]
    version = resource["version"]
    
    # Check if registered in static_config.go
    is_registered = kind in registered_kinds
    
    if is_registered:
        # Step 2.2: Update Completed
        resource["state"] = "Completed"
        resource["steps"] = {
            "gen-types": True,
            "identity-reference": True,
            "mapper-fuzzer": True,
            "mocks": True,
            "controller": True,
            "tests": True
        }
        resource["stage"] = "Stage 5 (Controller Implemented)"
        resource["trackingIssue"] = ""
        resource["assignee"] = ""
        resource["notes"] = ""
    else:
        # Step 2.3: Revert/ensure state is NOT marked as Completed
        if resource["state"] == "Completed":
            # Revert to In Progress or Not Started based on files
            _, temp_stage = determine_stages(group, kind, version)
            if temp_stage != "Investigation/Setup":
                resource["state"] = "In Progress"
            else:
                resource["state"] = "Not Started"
                
        # Handle tracking issues (Step 3)
        overseers = overseer_by_kind.get(kind, [])
        open_overseers = [i for i in overseers if i["state"] == "open"]
        
        if open_overseers:
            open_overseers.sort(key=lambda x: x["number"], reverse=True)
            main_issue = open_overseers[0]
            resource["state"] = "In Progress"
            resource["trackingIssue"] = f"[#{main_issue['number']}]({main_issue['url']})"
            resource["assignee"] = ", ".join(a["login"] for a in main_issue["assignees"])
            tracking_issue_num = main_issue["number"]
        else:
            resource["trackingIssue"] = "N/A"
            resource["assignee"] = ""
            tracking_issue_num = None
            
        # Determine physical stage
        steps, stage = determine_stages(group, kind, version)
        resource["steps"] = steps
        resource["stage"] = stage
        
        if stage != "Investigation/Setup":
            resource["state"] = "In Progress"
            
        # Step 3.2: Get external work
        matched_issues = get_external_work(open_issues, kind, all_kinds_sorted, tracking_issue_num)
        matched_prs = get_external_work(open_prs, kind, all_kinds_sorted, tracking_issue_num)
        
        if matched_issues or matched_prs:
            resource["state"] = "In Progress"
            
        # Parse manual/existing notes
        base_notes_list = []
        existing_notes = resource.get("notes", "")
        if existing_notes:
            parts = [p.strip() for p in existing_notes.split(",") if p.strip()]
            for p in parts:
                if p == "Missing _reference.go or _identity.go":
                    continue
                if "is closed but direct controller is not registered in code" in p:
                    continue
                if p.startswith("External Work:"):
                    continue
                base_notes_list.append(p)
                
        dynamic_notes = []
        
        # Add closed tracking issue anomaly notes
        if tracking_issue_num is None:
            closed_overseers = [i for i in overseers if i["state"] == "closed"]
            if closed_overseers:
                closed_overseers.sort(key=lambda x: x["number"], reverse=True)
                latest_closed = closed_overseers[0]
                dynamic_notes.append(f"Tracking issue #{latest_closed['number']} is closed but direct controller is not registered in code")
                
        # Add "Missing _reference.go or _identity.go" note if stage >= 4
        # Wait, let's verify if _identity.go and _reference.go exist
        has_id_file = False
        has_ref_file = False
        for f in all_apis_files:
            path_parts = [p.lower() for p in f.split(os.sep)]
            if group.lower() in path_parts and version.lower() in path_parts:
                if matches_kind(f, group, kind):
                    filename = os.path.basename(f).lower()
                    if filename.endswith("_identity.go"):
                        has_id_file = True
                    elif filename.endswith("_reference.go"):
                        has_ref_file = True
                        
        # Check Stage based on our steps/stage output
        # If mock/tests is True (meaning Stage >= 4), check if files are missing
        if steps["mocks"] or steps["controller"]:
            if not has_id_file and not has_ref_file:
                dynamic_notes.append("Missing _reference.go or _identity.go")
                
        # Add External Work notes
        external_works = []
        for item in matched_issues + matched_prs:
            external_works.append(f"External Work: #{item['number']}")
            
        # Deduplicate
        seen_ext = set()
        unique_ext_works = []
        for ext in external_works:
            if ext not in seen_ext:
                seen_ext.add(ext)
                unique_ext_works.append(ext)
                
        dynamic_notes.extend(unique_ext_works)
        
        # Combine
        resource["notes"] = ", ".join(base_notes_list + dynamic_notes)

# Step 6: Save Local Tracking Data
with open(data_path, "w") as f:
    json.dump(tracker_data, f, indent=2)
print("Saved data.json successfully.")

# Step 5: Identify Next Pending Resources
completed_kinds = {item["kind"] for item in tracker_data if item["state"] == "Completed"}
pending_candidates = []
for item in tracker_data:
    if item["state"] == "Not Started" and item.get("defaultController") in ("Terraform", "DCL"):
        deps_met = True
        for dep in item.get("dependencies", []):
            if dep not in completed_kinds:
                deps_met = False
                break
        if deps_met:
            pending_candidates.append(item)

pending_candidates.sort(key=lambda x: x.get("sortOrder", 9999))

# Step 7: Construct summary comment body
completed_count = sum(1 for item in tracker_data if item["state"] == "Completed")
in_progress_count = sum(1 for item in tracker_data if item["state"] == "In Progress")
pending_count = sum(1 for item in tracker_data if item["state"] == "Not Started")
total_count = len(tracker_data)

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

in_progress_resources = [item for item in tracker_data if item["state"] == "In Progress"]
# Sort in progress resources alphabetically by Kind
in_progress_resources.sort(key=lambda x: x["kind"])

for item in in_progress_resources:
    tracking_link = item.get("trackingIssue", "N/A")
    if tracking_link == "":
        tracking_link = "N/A"
    summary_body += f"| {item['kind']} | {item['stage']} | {tracking_link} | {item['assignee']} | {item['notes']} |\n"

summary_body += """
## Next Resources (Pending & Unblocked)
| Kind | Sort Order | Default Controller | Dependencies | Notes |
|------|------------|--------------------|--------------|-------|
"""

for item in pending_candidates[:20]: # Show up to 20 next unblocked candidates
    deps_str = ", ".join(item.get("dependencies", []))
    summary_body += f"| {item['kind']} | {item['sortOrder']} | {item['defaultController']} | {deps_str} | {item['notes']} |\n"

summary_body += """
## Completed Resources
| Kind | Default Controller | Date Completed / Notes |
|------|--------------------|------------------------|
"""

completed_resources = [item for item in tracker_data if item["state"] == "Completed"]
# Sort completed resources alphabetically by Kind
completed_resources.sort(key=lambda x: x["kind"])

for item in completed_resources:
    summary_body += f"| {item['kind']} | {item['defaultController']} | Registered in code |\n"

# Write body to comment_body.md for manual review or debugging
with open("dev/migration-tracker/comment_body.md", "w") as f:
    f.write(summary_body)

print("Constructed summary comment body and saved to dev/migration-tracker/comment_body.md")
