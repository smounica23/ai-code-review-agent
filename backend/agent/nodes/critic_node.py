from agent.state import AgentState
from services.llm_client import get_llm, invoke_llm
from agent.prompts.templates import CRITIC_SYSTEM_PROMPT
from langchain_core.messages import SystemMessage, HumanMessage
from services.json_utils import extract_json
import json

def critic_node(state:AgentState) -> dict:
    print("Critic node running...")

    llm = get_llm()
    context = "\n".join(state["retrieved_context"][:3])
    messages = [
        SystemMessage(content=CRITIC_SYSTEM_PROMPT),
        HumanMessage(content=f"""
Code:
{state["code"]}

Review findings:
{json.dumps(state["all_issues"])}

Evaluate the review quality and return JSON.
""")
    ]

    response = invoke_llm(llm, messages, "critic_node")
    try:
        result = extract_json(response.content)
        score = float(result.get("quality_score", 7))
    except (json.JSONDecodeError, ValueError):
        score = 7.0
    return {
        "quality_score": score, "retry_count": state.get("retry_count", 0) + 1
    }
