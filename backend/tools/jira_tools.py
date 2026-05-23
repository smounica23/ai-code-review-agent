import requests
from config import settings


def fetch_jira_ticket(ticket_id: str) -> dict :
    url = f"{settings.jira_base_url}/rest/api/3/issue/{ticket_id}"

    response = requests.get(
        url,
        headers={"Accept": "application/json"},
        auth=(settings.jira_email, settings.jira_api_token),
        timeout=20
    )
    data = response.json()
    fields = data["fields"]

    summary = fields["summary"]
    description = extract_text_from_adf(fields.get("description"))
    status = fields["status"]["name"]
    assignee = fields.get("assignee", {})
    assignee_name = assignee.get("displayName", "Unassigned") if assignee else "Unassigned"
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