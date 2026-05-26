from agent.state import AgentState
from services.llm_client import get_llm, invoke_llm
from agent.prompts.templates import LOGIC_REVIEW_PROMPT
from langchain_core.messages import SystemMessage, HumanMessage
from services.json_utils import extract_json
import json

def logic_review_node(state: AgentState) -> dict:
    print("Logic Review node running...")
    llm = get_llm()
    
    jira_context = ""
    if state.get("jira_ticket"):
        ticket = state["jira_ticket"]
        jira_context = f"""
Jira Ticket: {ticket["summary"]}
Description: {ticket["description"]}
"""

    messages = [
        SystemMessage(content=LOGIC_REVIEW_PROMPT),
        HumanMessage(content=f"""
Language: {state["language"]}
{jira_context}
Code to review:
{state["code"]}

Return ONLY a JSON array.
""")
    ]
    
    response = invoke_llm(llm, messages, "logic_review_node")
    issues = extract_json(response.content, default=[])
    return {"logic_issues": issues}