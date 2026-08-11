import json
import re
import os
import subprocess

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def main():
    # 1. Parse static_config.go
    direct_registered = {}
    with open('pkg/controller/resourceconfig/static_config.go', 'r') as f:
        for line in f:
            if 'Group:' in line and 'Kind:' in line:
                group_match = re.search(r'Group:\s*"([^"]+)"', line)
                kind_match = re.search(r'Kind:\s*"([^"]+)"', line)
                if group_match and kind_match:
                    gp = group_match.group(1).split('.')[0]
                    kd = kind_match.group(1)
                    has_direct = 'ReconcilerTypeDirect' in line
                    direct_registered[(gp, kd)] = has_direct

    # 2. Parse overseer issues
    with open('/tmp/overseer_issues.json', 'r') as f:
        overseer_issues = json.load(f)

    # 3. Parse open issues and PRs (SET 2)
    with open('/tmp/open_issues.json', 'r') as f:
        open_issues = json.load(f)
    with open('/tmp/open_prs.json', 'r') as f:
        open_prs = json.load(f)

    # 4. Load data.json
    with open('dev/migration-tracker/data.json', 'r') as f:
        data = json.load(f)

    kinds = [item['kind'] for item in data]
    sorted_kinds = sorted(kinds, key=len, reverse=True)

    # Helper function to determine stage, steps, is_stage2
    def determine_stage_and_steps(service, kind, version):
        kind_lowercase = kind.lower()
        
        # Stage 5
        stage5_files = [
            f"pkg/controller/direct/{service}/{kind_lowercase}_controller.go",
            f"pkg/controller/direct/{service}/{kind}_controller.go",
            f"pkg/controller/direct/{service}/adapter.go"
        ]
        is_stage5 = any(os.path.exists(f) for f in stage5_files)
        
        # Stage 4
        is_stage4 = False
        if os.path.exists(f"mockgcp/mock{service}"):
            is_stage4 = True
        if os.path.exists(f"pkg/controller/direct/{service}"):
            for f in os.listdir(f"pkg/controller/direct/{service}"):
                if "test" in f.lower() or "fixture" in f.lower():
                    is_stage4 = True
                    break
        # Check basic fixtures
        basic_dir = f"pkg/test/resourcefixture/testdata/basic/{service}"
        if os.path.exists(basic_dir):
            for root, dirs, files in os.walk(basic_dir):
                for d in dirs:
                    if d.lower() == kind_lowercase:
                        is_stage4 = True
                        break

        # Stage 3
        is_stage3 = os.path.exists(f"pkg/controller/direct/{service}/{kind_lowercase}_fuzzer.go") or \
                    os.path.exists(f"pkg/controller/direct/{service}/{kind}_fuzzer.go")

        # Stage 2
        is_stage2 = os.path.exists(f"apis/{service}/{version}/{kind_lowercase}_identity.go") or \
                    os.path.exists(f"apis/{service}/{version}/{kind_lowercase}_reference.go") or \
                    os.path.exists(f"apis/{service}/{version}/{kind}_identity.go") or \
                    os.path.exists(f"apis/{service}/{version}/{kind}_reference.go")

        # Stage 1
        is_stage1 = os.path.exists(f"apis/{service}/{version}/{kind_lowercase}_types.go") or \
                    os.path.exists(f"apis/{service}/{version}/{kind}_types.go")

        stage = "Investigation/Setup"
        steps = {
            "gen-types": False,
            "identity-reference": False,
            "mapper-fuzzer": False,
            "mocks": False,
            "controller": False,
            "tests": False
        }

        if is_stage5:
            stage = "Stage 5 (Controller Implemented)"
            steps = {
                "gen-types": True,
                "identity-reference": is_stage2,
                "mapper-fuzzer": is_stage3,
                "mocks": True,
                "controller": True,
                "tests": True
            }
        elif is_stage4:
            stage = "Stage 4 (MockGCP/E2E Fixtures)"
            steps = {
                "gen-types": True,
                "identity-reference": is_stage2,
                "mapper-fuzzer": is_stage3,
                "mocks": True,
                "controller": False,
                "tests": True
            }
        elif is_stage3:
            stage = "Stage 3 (KRM Fuzzer)"
            steps = {
                "gen-types": True,
                "identity-reference": is_stage2,
                "mapper-fuzzer": True,
                "mocks": False,
                "controller": False,
                "tests": False
            }
        elif is_stage2:
            stage = "Stage 2 (Identity & Reference Types)"
            steps = {
                "gen-types": True,
                "identity-reference": True,
                "mapper-fuzzer": False,
                "mocks": False,
                "controller": False,
                "tests": False
            }
        elif is_stage1:
            stage = "Stage 1 (Direct KRM Types)"
            steps = {
                "gen-types": True,
                "identity-reference": False,
                "mapper-fuzzer": False,
                "mocks": False,
                "controller": False,
                "tests": False
            }

        return stage, steps, is_stage2

    # Parse Kind out of issue titles for overseer
    overseer_issues_by_kind = {}
    for issue in overseer_issues:
        title = issue['title']
        # Sort kinds by length descending to match longer ones first
        matched_kind = None
        for kind in sorted_kinds:
            pattern = r'\b' + re.escape(kind) + r'\b'
            if re.search(pattern, title, re.IGNORECASE):
                matched_kind = kind
                break
        if matched_kind:
            overseer_issues_by_kind[matched_kind] = issue

    # Collect active issue/PR mappings for uncompleted Kinds (SET 2)
    overseer_issue_numbers = {issue['number'] for issue in overseer_issues}
    external_works_by_kind = {}

    def get_author_login(item):
        if 'author' in item and isinstance(item['author'], dict):
            return item['author'].get('login', '').lower()
        return ''

    for issue in open_issues:
        author = get_author_login(issue)
        if 'bot' in author or 'robot' in author:
            continue
        if issue['number'] in overseer_issue_numbers:
            continue
        title = issue['title']
        for kind in sorted_kinds:
            pattern = r'\b' + re.escape(kind) + r'\b'
            if re.search(pattern, title, re.IGNORECASE):
                external_works_by_kind.setdefault(kind, set()).add(issue['number'])

    for pr in open_prs:
        author = get_author_login(pr)
        if 'bot' in author or 'robot' in author:
            continue
        title = pr['title']
        for kind in sorted_kinds:
            pattern = r'\b' + re.escape(kind) + r'\b'
            if re.search(pattern, title, re.IGNORECASE):
                external_works_by_kind.setdefault(kind, set()).add(pr['number'])

    # Helper function to compute merged notes
    def generate_notes(existing_notes, is_missing_ref_id, closed_tracking_issue_anomaly=None, external_works=None):
        notes_list = []
        if closed_tracking_issue_anomaly:
            notes_list.append(closed_tracking_issue_anomaly)
        if is_missing_ref_id:
            notes_list.append("Missing _reference.go or _identity.go")
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
                notes_list.append(note)
        if external_works:
            for ew in sorted(list(external_works)):
                notes_list.append(f"External Work: #{ew}")
        return ", ".join(notes_list)

    # Process each resource in data.json
    for item in data:
        gp = item['group']
        kd = item['kind']
        version = item['version']
        key = (gp, kd)
        is_direct = direct_registered.get(key, False)

        # Stage and step verification
        stage, steps, is_stage2 = determine_stage_and_steps(gp, kd, version)

        # Missing reference / identity warning if types exist but Stage 2 doesn't
        # Check if gen-types is True, but identity-reference is False
        is_missing_ref_id = False
        if stage != "Investigation/Setup" and not is_stage2:
            is_missing_ref_id = True

        if is_direct:
            # Step 2: Registered in code -> Completed
            item['state'] = "Completed"
            item['stage'] = "Stage 5 (Controller Implemented)"
            item['trackingIssue'] = ""
            item['assignee'] = ""
            item['notes'] = ""
            item['steps'] = {
                "gen-types": True,
                "identity-reference": True,
                "mapper-fuzzer": True,
                "mocks": True,
                "controller": True,
                "tests": True
            }
            if "Direct" not in item['supportedControllers']:
                item['supportedControllers'].append("Direct")
        else:
            # Revert/set back from Completed if it isn't registered
            if item['state'] == "Completed":
                if stage != "Investigation/Setup":
                    item['state'] = "In Progress"
                else:
                    item['state'] = "Not Started"

            # Parse overseer issues
            overseer_issue = overseer_issues_by_kind.get(kd, None)
            closed_tracking_issue_anomaly = None
            if overseer_issue:
                if overseer_issue['state'] == 'OPEN':
                    item['state'] = "In Progress"
                    item['trackingIssue'] = f"[#{overseer_issue['number']}]({overseer_issue['url']})"
                    item['assignee'] = ", ".join(a['login'] for a in overseer_issue['assignees'])
                else: # CLOSED
                    item['trackingIssue'] = "N/A"
                    item['assignee'] = ""
                    closed_tracking_issue_anomaly = f"Tracking issue #{overseer_issue['number']} is closed but direct controller is not registered in code"
                    if stage != "Investigation/Setup":
                        item['state'] = "In Progress"
                    else:
                        item['state'] = "Not Started"
            else:
                item['trackingIssue'] = "N/A"
                item['assignee'] = ""

            # Check for other external issues (SET 2)
            ext_works = external_works_by_kind.get(kd, None)
            if ext_works:
                item['state'] = "In Progress"

            # Update stage and steps
            item['stage'] = stage
            item['steps'] = steps

            # Generate and merge notes
            item['notes'] = generate_notes(item.get('notes', ''), is_missing_ref_id, closed_tracking_issue_anomaly, ext_works)

    # Step 5: Identify Next Pending Resources
    completed_kinds = {item['kind'] for item in data if item['state'] == 'Completed'}
    pending_candidates = []
    for item in data:
        if item['state'] == 'Not Started' and item['defaultController'] in ('Terraform', 'DCL'):
            deps = item.get('dependencies', [])
            all_deps_completed = True
            for dep in deps:
                dep_in_data = any(x['kind'] == dep for x in data)
                if dep_in_data and dep not in completed_kinds:
                    all_deps_completed = False
                    break
            if all_deps_completed:
                pending_candidates.append(item)

    pending_candidates.sort(key=lambda x: x['sortOrder'])

    # Step 6: Save local tracking data to dev/migration-tracker/data.json
    with open('dev/migration-tracker/data.json', 'w') as f:
        json.dump(data, f, indent=2)

    print("Successfully processed and saved dev/migration-tracker/data.json")

    # Step 7: Update Summary Comment on Coordinator Issue
    completed_count = sum(1 for item in data if item['state'] == 'Completed')
    in_progress_count = sum(1 for item in data if item['state'] == 'In Progress')
    pending_count = sum(1 for item in data if item['state'] == 'Not Started')
    total_count = len(data)

    # Format Markdown
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
    # Sort In Progress resources alphabetically by Kind
    in_progress_items = sorted([item for item in data if item['state'] == 'In Progress'], key=lambda x: x['kind'])
    for item in in_progress_items:
        assignee_str = item.get('assignee', '')
        summary_body += f"| {item['kind']} | {item['stage']} | {item['trackingIssue']} | {assignee_str} | {item['notes']} |\n"

    summary_body += """
## Next Resources (Pending & Unblocked)
| Kind | Sort Order | Default Controller | Dependencies | Notes |
|------|------------|--------------------|--------------|-------|
"""
    for item in pending_candidates:
        deps_str = ", ".join(item.get('dependencies', []))
        summary_body += f"| {item['kind']} | {item['sortOrder']} | {item['defaultController']} | {deps_str} | {item['notes']} |\n"

    summary_body += """
## Completed Resources
| Kind | Default Controller | Date Completed / Notes |
|------|--------------------|------------------------|
"""
    # Sort Completed resources alphabetically by Kind
    completed_items = sorted([item for item in data if item['state'] == 'Completed'], key=lambda x: x['kind'])
    for item in completed_items:
        summary_body += f"| {item['kind']} | {item['defaultController']} | Registered in code |\n"

    # Write summary body to a temporary file
    with open('/tmp/summary_comment.md', 'w') as f:
        f.write(summary_body)

    print("Generated progress summary report in /tmp/summary_comment.md")

if __name__ == "__main__":
    main()
