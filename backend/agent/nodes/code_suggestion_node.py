from agent.state import AgentState
from services.llm_client import get_llm, invoke_llm
from agent.prompts.templates import CODE_SUGGESTION_PROMPT
from langchain_core.messages import SystemMessage, HumanMessage
from services.json_utils import extract_json
import json


def code_suggestion_node(state:AgentState) -> dict:
    if not state["alignment_issues"] or not state.get("jira_ticket"):
        return {"code_suggestions": []}
    
    llm = get_llm()
    messages = [SystemMessage(content=CODE_SUGGESTION_PROMPT),
    HumanMessage(content=f"""Jira Ticket Summary: {state["jira_ticket"]["summary"]}
        Jira Description: {state["jira_ticket"]["description"]}
        Language : {state["language"]}
        Missing requirements : {json.dumps(state["alignment_issues"])}
        Existing Code: {state["code"]},
        """)]
    
    response = invoke_llm(llm, messages, "code_suggestion_node")
    print("RAW:", response.content[:500])  # add this
    code_suggestions = extract_json(response.content, default=[])
    return {"code_suggestions": code_suggestions}

