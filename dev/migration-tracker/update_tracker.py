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
from collections import defaultdict

def run_gh(args):
    cmd = ["gh"] + args
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"Error running {' '.join(cmd)}: {res.stderr}", file=sys.stderr)
        return []
    try:
        return json.loads(res.stdout)
    except Exception as e:
        print(f"Error parsing JSON from {' '.join(cmd)}: {e}", file=sys.stderr)
        return []

def get_implemented_types(apis_dir="../../apis"):
    implemented_kinds = {}
    struct_regex = re.compile(r"type\s+([A-Za-z0-9_]+)\s+struct\s*\{")
    if not os.path.exists(apis_dir):
        return implemented_kinds

    for root, _, files in os.walk(apis_dir):
        for file in files:
            if file.endswith("_types.go"):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    matches = struct_regex.findall(content)
                    for kind in matches:
                        if kind.endswith("Spec") or kind.endswith("Status") or kind.endswith("List") or kind.endswith("ObservedState"):
                            continue
                        if kind not in implemented_kinds:
                            implemented_kinds[kind] = []
                        implemented_kinds[kind].append(filepath)
    return implemented_kinds

def get_implemented_controllers(direct_dir="../../pkg/controller/direct"):
    implemented_controllers = set()
    if not os.path.exists(direct_dir):
        return implemented_controllers
    for root, _, files in os.walk(direct_dir):
        for file in files:
            if file.endswith("_controller.go"):
                implemented_controllers.add(file)
    return implemented_controllers

def parse_static_config(config_file_path="../../pkg/controller/resourceconfig/static_config.go"):
    static_configs = {}
    if not os.path.exists(config_file_path):
        return static_configs
        
    with open(config_file_path, 'r') as f:
        config_lines = f.readlines()
        
    for line in config_lines:
        line = line.strip()
        if not line.startswith('{Group: '):
            continue
            
        group_match = re.search(r'Group:\s*"([^"]+)"', line)
        kind_match = re.search(r'Kind:\s*"([^"]+)"', line)
        default_ctrl_match = re.search(r'DefaultController:\s*k8s\.ReconcilerType([A-Za-z]+)', line)
        supported_ctrls_match = re.search(r'SupportedControllers:\s*\[\]k8s\.ReconcilerType\{(.*?)\}', line)
        
        if group_match and kind_match:
            kind = kind_match.group(1)
            supported = []
            if supported_ctrls_match:
                ctrls_raw = supported_ctrls_match.group(1)
                supported = re.findall(r'k8s\.ReconcilerType([A-Za-z]+)', ctrls_raw)
            
            default_ctrl = "Unknown"
            if default_ctrl_match:
                default_ctrl = default_ctrl_match.group(1)
                
            static_configs[kind] = {
                "supported": supported,
                "default": default_ctrl
            }
    return static_configs

def matches_kind(kind, text):
    text_lower = text.lower()
    kind_lower = kind.lower()
    if kind_lower not in text_lower:
        return False
    
    # Generic short/common kinds
    if kind in ["Service", "Project", "Folder", "Run"]:
        pattern = rf"\b{re.escape(kind)}\b"
        if not re.search(pattern, text):  # Case-sensitive whole-word
            # Check also lowercase with word boundary
            pattern_lower = rf"\b{re.escape(kind_lower)}\b"
            if not re.search(pattern_lower, text):
                return False
    return True

def generate_summary(resources):
    completed = [r for r in resources if r['state'] == "Completed"]
    in_progress = [r for r in resources if r['state'] == "In Progress"]
    not_started = [r for r in resources if r['state'] == "Not Started"]
    
    completed_count = len(completed)
    in_progress_count = len(in_progress)
    pending_count = len(not_started)
    total_count = len(resources)
    
    md = []
    md.append("### Migration Progress Tracker Summary\n")
    md.append("## High-Level Status")
    md.append("| State | Count |")
    md.append("|-------|-------|")
    md.append(f"| Completed | {completed_count} |")
    md.append(f"| In Progress | {in_progress_count} |")
    md.append(f"| Pending | {pending_count} |")
    md.append(f"| Total | {total_count} |\n")
    
    md.append("## In Progress Resources")
    md.append("| Kind | Current Stage | Tracking Issue/PR | Assignee | Notes |")
    md.append("|------|---------------|-------------------|----------|-------|")
    for r in sorted(in_progress, key=lambda x: x['kind']):
        issue_link = "N/A"
        if r.get('trackingIssue'):
            m = re.search(r"/issues/(\d+)", r['trackingIssue'])
            if m:
                issue_link = f"[#{m.group(1)}]({r['trackingIssue']})"
            else:
                issue_link = f"[Link]({r['trackingIssue']})"
        assignee = r.get('assignee', '')
        notes = r.get('notes', '')
        md.append(f"| {r['kind']} | {r['stage']} | {issue_link} | {assignee} | {notes} |")
    md.append("")
    
    # Next Resources (Pending & Unblocked)
    completed_kinds = {r['kind'] for r in completed}
    next_resources = []
    for r in not_started:
        if r.get('defaultController') in ("Terraform", "DCL"):
            deps = r.get('dependencies', [])
            # All deps must be in completed_kinds
            if all(dep in completed_kinds for dep in deps):
                next_resources.append(r)
                
    next_resources = sorted(next_resources, key=lambda x: x['sortOrder'])
    
    md.append("## Next Resources (Pending & Unblocked)")
    md.append("| Kind | Sort Order | Default Controller | Dependencies | Notes |")
    md.append("|------|------------|--------------------|--------------|-------|")
    for r in next_resources:
        deps_str = ", ".join(r.get('dependencies', []))
        notes = r.get('notes', '')
        md.append(f"| {r['kind']} | {r['sortOrder']} | {r.get('defaultController', '')} | {deps_str} | {notes} |")
    md.append("")
    
    md.append("## Completed Resources")
    md.append("| Kind | Default Controller | Date Completed / Notes |")
    md.append("|------|--------------------|------------------------|")
    for r in sorted(completed, key=lambda x: x['kind']):
        notes = r.get('notes', '')
        if not notes:
            notes = "Registered in code"
        md.append(f"| {r['kind']} | {r.get('defaultController', '')} | {notes} |")
        
    return "\n".join(md)

def update_comment_on_github(summary_body, coordinator_issue="10588"):
    comments_data = run_gh(["issue", "view", coordinator_issue, "--json", "comments"])
    
    comment_id = None
    if isinstance(comments_data, dict) and "comments" in comments_data:
        for c in comments_data["comments"]:
            if "### Migration Progress Tracker Summary" in c.get("body", ""):
                html_url = c.get("url", "")
                m = re.search(r"#issuecomment-(\d+)", html_url)
                if m:
                    comment_id = m.group(1)
                else:
                    comment_id = c.get("id")
                break
                
    if comment_id:
        print(f"Editing existing comment {comment_id} on issue {coordinator_issue}...")
        with open("temp_comment.md", "w") as f:
            f.write(summary_body)
        
        cmd = ["gh", "api", "-X", "PATCH", f"repos/GoogleCloudPlatform/k8s-config-connector/issues/comments/{comment_id}", "-F", "body=@temp_comment.md"]
        subprocess.run(cmd, check=True)
        os.remove("temp_comment.md")
        print("Successfully updated comment!")
    else:
        print("Posting new comment...")
        with open("temp_comment.md", "w") as f:
            f.write(summary_body)
        cmd = ["gh", "issue", "comment", "create", coordinator_issue, "-F", "temp_comment.md"]
        subprocess.run(cmd, check=True)
        os.remove("temp_comment.md")
        print("Successfully posted new comment!")

def main():
    apis_dir = "../../apis"
    direct_dir = "../../pkg/controller/direct"
    static_config_path = "../../pkg/controller/resourceconfig/static_config.go"
    data_json_path = "data.json"
    
    # 1. Load data.json
    if not os.path.exists(data_json_path):
        print(f"Error: {data_json_path} does not exist.", file=sys.stderr)
        sys.exit(1)
        
    with open(data_json_path, 'r') as f:
        resources = json.load(f)
        
    all_kinds = [res['kind'] for res in resources]
    resource_by_kind = {res['kind']: res for res in resources}
    
    # 2. Parse static_config.go
    static_configs = parse_static_config(static_config_path)
    
    # 3. Get implemented types and controllers
    implemented_types = get_implemented_types(apis_dir)
    implemented_controllers = get_implemented_controllers(direct_dir)
    
    # 4. Fetch GitHub Overseer/Migrate Issues (SET 1)
    print("Fetching active overseer/migrate issues...")
    overseer_issues = run_gh(["issue", "list", "--state", "all", "--label", "overseer,workflow/migrate", "--limit", "300", "--json", "number,title,labels,assignees,state,url"])
    
    kind_to_overseer_issue = {}
    for issue in overseer_issues:
        title = issue.get("title", "")
        # Try to find a matching Kind for this issue title
        matched_kind = None
        title_lower = title.lower()
        for k in sorted(all_kinds, key=len, reverse=True):
            if k.lower() in title_lower:
                matched_kind = k
                break
        if matched_kind:
            # We prefer open issues over closed ones, or the newest one
            existing = kind_to_overseer_issue.get(matched_kind)
            if not existing or (existing.get("state") == "CLOSED" and issue.get("state") == "OPEN"):
                kind_to_overseer_issue[matched_kind] = issue

    # 5. Fetch ALL Open Issues and PRs in the Repository (SET 2)
    print("Fetching all open issues and PRs for external work detection...")
    open_issues = run_gh(["issue", "list", "--state", "open", "--limit", "2000", "--json", "number,title,url,assignees,author,state"])
    open_prs = run_gh(["pr", "list", "--state", "open", "--limit", "2000", "--json", "number,title,url,author,state"])
    
    # We filter out bots (author login has "bot" or "robot")
    external_issues_and_prs = []
    for item in open_issues + open_prs:
        author_login = item.get("author", {}).get("login", "").lower()
        if "bot" in author_login or "robot" in author_login:
            continue
        # Also skip tracker issue 10588
        if item.get("number") == 10588:
            continue
        external_issues_and_prs.append(item)

    # 6. Process each resource
    for res in resources:
        kind = res['kind']
        group = res['group']
        version = res.get('version', 'v1beta1')
        
        # Determine static registration
        cfg = static_configs.get(kind, {})
        supported_ctrls = cfg.get("supported", [])
        default_ctrl = cfg.get("default", "Unknown")
        
        res['supportedControllers'] = supported_ctrls
        if default_ctrl != "Unknown":
            res['defaultController'] = default_ctrl
            res['controllerType'] = default_ctrl
            
        is_direct_registered = "Direct" in supported_ctrls
        
        # Compute files existence
        has_types = kind in implemented_types
        has_id_ref = False
        has_fuzzer = False
        has_ctrl = False
        prefix = kind.lower()
        
        if has_types:
            res['steps']['gen-types'] = True
            for filepath in implemented_types[kind]:
                dirpath = os.path.dirname(filepath)
                filename = os.path.basename(filepath)
                prefix = filename.replace("_types.go", "")
                
                possible_id_ref_names = [
                    f"{prefix}_reference.go",
                    f"{prefix}_identity.go",
                    f"{kind.lower()}_reference.go",
                    f"{kind.lower()}_identity.go",
                ]
                for name in possible_id_ref_names:
                    if os.path.exists(os.path.join(dirpath, name)):
                        has_id_ref = True
                        break
                        
                possible_mapper_names = [
                    f"{prefix}_mapper.go",
                    f"{prefix}_fuzzer.go",
                    f"{kind.lower()}_mapper.go",
                    f"{kind.lower()}_fuzzer.go",
                ]
                for name in possible_mapper_names:
                    if os.path.exists(os.path.join(dirpath, name)):
                        has_fuzzer = True
                        break
                if has_id_ref and has_fuzzer:
                    break
        else:
            res['steps']['gen-types'] = False
            
        res['steps']['identity-reference'] = has_id_ref
        res['steps']['mapper-fuzzer'] = has_fuzzer
        
        possible_controller_names = [
            f"{kind.lower()}_controller.go",
            f"{group.lower()}{kind.lower()}_controller.go",
            f"{prefix}_controller.go"
        ]
        for ctrl_name in possible_controller_names:
            if ctrl_name in implemented_controllers:
                has_ctrl = True
                break
                
        res['steps']['controller'] = has_ctrl
        
        has_mock = os.path.exists(f"../../mockgcp/mock{group}")
        res['steps']['mocks'] = has_mock
        
        # Check active tracking issue
        tracking_issue = kind_to_overseer_issue.get(kind)
        tracking_issue_url = ""
        assignee_login = ""
        anomaly_note = ""
        
        if tracking_issue:
            issue_state = tracking_issue.get("state")
            issue_num = tracking_issue.get("number")
            issue_url = tracking_issue.get("url")
            
            if issue_state == "OPEN":
                if not is_direct_registered:
                    tracking_issue_url = issue_url
                    assignees = tracking_issue.get("assignees", [])
                    if assignees:
                        assignee_login = assignees[0].get("login", "")
            else:  # CLOSED
                if not is_direct_registered:
                    anomaly_note = f"Tracking issue #{issue_num} is closed but direct controller is not registered in code"

        res['trackingIssue'] = tracking_issue_url
        res['assignee'] = assignee_login
        
        # Find external work (SET 2)
        external_mentions = []
        for item in external_issues_and_prs:
            item_title = item.get("title", "")
            item_url = item.get("url", "")
            item_num = item.get("number")
            
            # Avoid attributing the same tracking issue as external work
            if tracking_issue and item_num == tracking_issue.get("number"):
                continue
                
            if matches_kind(kind, item_title):
                is_pr = "pull" in item_url
                label = f"#{item_num}"
                external_mentions.append(label)
                
        # Build Notes
        notes_parts = []
        if not has_id_ref and has_types:
            notes_parts.append("Missing _reference.go or _identity.go")
            
        if anomaly_note:
            notes_parts.append(anomaly_note)
            
        if external_mentions:
            for mention in sorted(list(set(external_mentions))):
                notes_parts.append(f"External Work: {mention}")
                
        res['notes'] = ", ".join(notes_parts)
        
        # Determine State
        if is_direct_registered:
            res['state'] = "Completed"
            res['steps']['tests'] = True
            res['steps']['mocks'] = True
            res['steps']['controller'] = True
            res['steps']['mapper-fuzzer'] = True
            res['steps']['identity-reference'] = True
            res['steps']['gen-types'] = True
        else:
            has_fixtures = False
            fixture_dir = f"../../pkg/test/resourcefixture/testdata/basic/{group}/{version}/{kind.lower()}"
            if os.path.exists(fixture_dir):
                has_fixtures = True
            else:
                basic_dir = "../../pkg/test/resourcefixture/testdata/basic"
                if os.path.exists(basic_dir):
                    for r, dirs, files in os.walk(basic_dir):
                        for d in dirs:
                            if d.lower() == kind.lower():
                                has_fixtures = True
                                break
                        if has_fixtures:
                            break
                            
            has_direct_tests = False
            g_dir = f"../../pkg/controller/direct/{group}"
            if os.path.exists(g_dir):
                for f in os.listdir(g_dir):
                    if f.endswith("_test.go"):
                        has_direct_tests = True
                        break
                        
            has_work = has_types or has_id_ref or has_fuzzer or has_ctrl or has_mock or has_fixtures or has_direct_tests or tracking_issue_url or external_mentions
            
            if has_work:
                res['state'] = "In Progress"
            else:
                res['state'] = "Not Started"
                
        # Determine Stage
        if res['state'] == "Completed":
            res['stage'] = "Stage 5 (Controller Implemented)"
        elif res['state'] == "In Progress":
            if has_ctrl:
                res['stage'] = "Stage 5 (Controller Implemented)"
            elif has_mock or has_fixtures or has_direct_tests:
                res['stage'] = "Stage 4 (MockGCP/E2E Fixtures)"
            elif has_fuzzer:
                res['stage'] = "Stage 3 (KRM Fuzzer)"
            elif has_id_ref:
                res['stage'] = "Stage 2 (Identity & Reference Types)"
            elif has_types:
                res['stage'] = "Stage 1 (Direct KRM Types)"
            else:
                inferred = False
                for mention in external_mentions + ([tracking_issue.get("title", "")] if tracking_issue else []):
                    mention_lower = mention.lower()
                    if "types.go" in mention_lower:
                        res['stage'] = "Stage 1 (Direct KRM Types)"
                        inferred = True
                        break
                    elif "identity" in mention_lower or "reference" in mention_lower:
                        res['stage'] = "Stage 2 (Identity & Reference Types)"
                        inferred = True
                        break
                    elif "fuzzer" in mention_lower:
                        res['stage'] = "Stage 3 (KRM Fuzzer)"
                        inferred = True
                        break
                if not inferred:
                    res['stage'] = "Investigation/Setup"
        else:
            res['stage'] = "Investigation/Setup"

    # Sort resources by Kind alphabetically
    resources = sorted(resources, key=lambda x: x['kind'])
    
    # 7. Write data.json
    with open(data_json_path, 'w') as f:
        json.dump(resources, f, indent=2)
    print(f"Saved {len(resources)} resources to {data_json_path}")
    
    # 8. Generate Summary and update Github
    summary_body = generate_summary(resources)
    update_comment_on_github(summary_body)

if __name__ == "__main__":
    main()
