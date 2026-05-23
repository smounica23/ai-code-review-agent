from agent.state import AgentState
from langchain_core.messages import SystemMessage, HumanMessage
from agent.prompts.templates import ALIGNMENT_SYSTEM_PROMPT
from services.llm_client import get_llm, invoke_llm
from services.json_utils import extract_json


def requirement_alignment_node(state:AgentState)->dict:
    if not state["jira_ticket_id"]:
       return {"alignment_issues": [], "alignment_score": 0.0}
    llm = get_llm()
    messages = [
        SystemMessage(content=ALIGNMENT_SYSTEM_PROMPT),
        HumanMessage(content=f"""Jira Ticket Summary: {state["jira_ticket"]["summary"]}
        Jira Description: {state["jira_ticket"]["description"]}

        Code to review:
        {state["code"]},
        """
        )
    ]

    response = invoke_llm(llm, messages, "requirement_alignment_node")
    result = extract_json(response.content, default={"criteria_met": [], "criteria_missed": [], "logic_issues": [], "alignment_score": 0.0})


    alignment_issues = result.get("criteria_missed", []) + result.get("logic_issues", [])
    alignment_score = float(result.get("alignment_score", 0.0))

    return {
        "alignment_issues": alignment_issues,
        "alignment_score": alignment_score
    }