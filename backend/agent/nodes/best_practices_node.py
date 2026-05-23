from agent.state import AgentState
from services.llm_client import get_llm, invoke_llm
from agent.prompts.templates import FIX_SUGGESTION_SYSTEM_PROMPT
from langchain_core.messages import SystemMessage, HumanMessage
from services.json_utils import extract_json 
import json

def best_practices_node(state: AgentState) -> dict:
    print("Best parctices node running...")
    llm = get_llm()

    # filter only HIGH and CRITICAL issues
    high_issues = [
        i for i in state["security_issues"] + state["performance_issues"]
        if i.get("severity") in ("CRITICAL", "HIGH")
    ]

    messages = [
        SystemMessage(content=FIX_SUGGESTION_SYSTEM_PROMPT),
        HumanMessage(content=f"""
Language: {state["language"]}
Issues that need fixes: {json.dumps(high_issues)}

Code:
```{state["language"]}
{state["code"]}
```

Return ONLY a JSON array with fix suggestions.
""")
    ]

    response = invoke_llm(llm, messages, "best_practices_node")
    try:
        fixes = extract_json(response.content)
    except json.JSONDecodeError:
        fixes = []

    all_issues = (
        state["security_issues"] +
        state["performance_issues"] +
        state["best_practice_issues"] +
        state["static_issues"]
    )

    return {"all_issues": all_issues}