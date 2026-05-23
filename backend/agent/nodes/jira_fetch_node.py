from agent.state import AgentState
from tools.jira_tools import fetch_jira_ticket

def jira_fetch_node(state: AgentState) -> dict:
    print("Jira Fetch node running...")
    
    ticket_id = state.get("jira_ticket_id")
    if not ticket_id:
        return {"jira_ticket": None}
    
    try:
        ticket = fetch_jira_ticket(ticket_id)
        return {"jira_ticket": ticket}
    except Exception as e:
        print(f"Jira fetch failed: {e}")
        return {"jira_ticket": None}