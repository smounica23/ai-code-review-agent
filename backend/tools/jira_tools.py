import requests
from config import settings


def fetch_jira_ticket(ticket_id: str) -> dict:
    url = f"{settings.jira_base_url}/rest/api/3/issue/{ticket_id}"

    response = requests.get(
        url,
        headers={"Accept": "application/json"},
        auth=(settings.jira_email, settings.jira_api_token),
        timeout=20
    )
    
    if response.status_code != 200:
        print(f"Jira API error: {response.status_code} — {response.text[:200]}")
        return None
    
    data = response.json()
    
    if "fields" not in data:
        print(f"Jira response missing fields: {data}")
        return None
    
    fields = data["fields"]
    summary = fields.get("summary", "")
    description = extract_text_from_adf(fields.get("description"))
    status = fields.get("status", {}).get("name", "Unknown")
    assignee = fields.get("assignee") or {}
    assignee_name = assignee.get("displayName", "Unassigned")
    
    return {
        "ticket_id": ticket_id,
        "summary": summary,
        "description": description,
        "status": status,
        "assignee": assignee_name
    }


def extract_text_from_adf(adf_doc) -> str:
    """Recursively extract plain text from Atlassian Document Format"""
    if not adf_doc:
        return ""
    text_parts = []
    if isinstance(adf_doc, dict):
        if adf_doc.get("type") == "text":
            text_parts.append(adf_doc.get("text", ""))
        for key in ["content", "children"]:
            if key in adf_doc:
                text_parts.append(extract_text_from_adf(adf_doc[key]))
    elif isinstance(adf_doc, list):
        for item in adf_doc:
            text_parts.append(extract_text_from_adf(item))
    return " ".join(filter(None, text_parts))