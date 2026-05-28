#!/usr/bin/env python3
"""
GitHub Actions review script.
Reads changed files, calls review API, exits 1 if critical issues found.
"""
import sys
import os
import json
import requests
import re


API_URL = os.getenv("REVIEW_API_URL", "http://localhost:8000/api/v1")

EXTENSION_MAP = {
    ".py": "python",
    ".java": "java", 
    ".js": "javascript"
}

def extract_jira_ticket_id(pr_title: str = "", pr_body: str = "") -> str | None:
    """Extract Jira ticket ID from PR title or body"""
    pattern = r'[A-Z]+-\d+'
    
    match = re.search(pattern, pr_title)
    if match:
        return match.group(0)
    
    match = re.search(pattern, pr_body)
    if match:
        return match.group(0)
    
    return None


def review_file(filepath: str, jira_ticket_id: str = None) -> dict | None:
    try:
        with open(filepath, encoding="utf-8") as f:
            code = f.read()
    except Exception as e:
        print(f"Could not read {filepath}: {e}")
        return None

    ext = "." + filepath.rsplit(".", 1)[-1]
    language = EXTENSION_MAP.get(ext)
    if not language:
        return None

    print(f"Reviewing {filepath} ({language})...")

    try:
        resp = requests.post(
            f"{API_URL}/review",
            json={"code": code, "language": language, "filename": filepath, "jira_ticket_id": jira_ticket_id},
            timeout=60
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Review failed for {filepath}: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: github_review.py <changed_files.txt>")
        sys.exit(0)
    pr_title = os.getenv("PR_TITLE", "")
    pr_body = os.getenv("PR_BODY", "")
    jira_ticket_id = extract_jira_ticket_id(pr_title, pr_body)
    if jira_ticket_id:
        print(f"Found Jira ticket: {jira_ticket_id}")
    else:
        print("No Jira ticket ID found in PR")
    with open(sys.argv[1]) as f:
        files = [line.strip() for line in f if line.strip()]

    if not files:
        print("No files to review.")
        sys.exit(0)

    all_issues = []
    overall_score = 10.0
    critical_count = 0
    alignment_issues = []
    alignment_score = 0.0
    logic_issues = []
    code_suggestions = [] 
    for filepath in files:
        if not os.path.exists(filepath):
            continue
        result = review_file(filepath, jira_ticket_id=jira_ticket_id)        
        if result:
            all_issues.extend(result.get("issues", []))
            critical_count += result.get("critical_count", 0)
            overall_score = min(overall_score, result.get("overall_score", 10.0))
            alignment_issues.extend(result.get("alignment_issues", []))
            alignment_score = result.get("alignment_score", 0.0)
            logic_issues.extend(result.get("logic_issues", [])) 
            code_suggestions.extend(result.get("code_suggestions", []))

    results = {
        "overall_score": overall_score,
        "critical_count": critical_count,
        "issues": all_issues,
        "jira_ticket_id": jira_ticket_id,
        "alignment_issues": alignment_issues,  
        "alignment_score": alignment_score,
        "logic_issues": logic_issues,
        "code_suggestions": code_suggestions
    }
    with open("review_results.json", "w") as f:
        json.dump(results, f)

    print(f"\n{'='*50}")
    print(f"Overall Score: {overall_score}/10")
    print(f"Critical Issues: {critical_count}")
    print(f"Total Issues: {len(all_issues)}")
    print(f"{'='*50}\n")

    if critical_count > 0:
        print(f"❌ {critical_count} critical issue(s) found. Fix before merging.")
        for issue in all_issues:
            if issue.get("severity") == "CRITICAL":
                print(f"  Line {issue.get('line_start')}: {issue.get('description')}")
        sys.exit(1)
    else:
        print("✅ No critical issues found.")
        sys.exit(0)

if __name__ == "__main__":
    main()