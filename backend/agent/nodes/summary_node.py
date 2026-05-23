from agent.state import AgentState
from services.llm_client import get_llm, invoke_llm
from agent.prompts.templates import SUMMARY_SYSTEM_PROMPT
from langchain_core.messages import SystemMessage, HumanMessage
from services.json_utils import extract_json
import json


def summary_node(state:AgentState) -> dict:
    print("Summary node running...")
    llm = get_llm()
    context = "\n".join(state["retrieved_context"][:3])
    messages = [
        SystemMessage(content=SUMMARY_SYSTEM_PROMPT),
        HumanMessage(content=f"""
        
AllIssues: {state["all_issues"]}
Code: {state["code"]}
Quality_score: {state.get("quality_score", 0.0)}

                     

                     """)
    ]

    response = invoke_llm(llm , messages, "summary_node")
    try:
        summary = extract_json(response.content)
        overall_score = float(summary.get("overall_score", 5.0))
        summary_text = summary.get("summary_text", "Review complete.")
    except (json.JSONDecodeError, ValueError):
        overall_score = 5.0
        summary_text = "Review complete."

    return {"overall_score": overall_score, "summary": summary_text}