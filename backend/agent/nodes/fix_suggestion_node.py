from agent.state import AgentState
from services.llm_client import get_llm, invoke_llm
from agent.prompts.templates import FIX_SUGGESTION_SYSTEM_PROMPT
from langchain_core.messages import SystemMessage, HumanMessage
from services.json_utils import extract_json
import json

def fix_suggestion_node(state:AgentState) -> dict:
    print("Fix Suggestion node running...")
    llm = get_llm()
    high_issues = [
        i for i in state["security_issues"] + state["performance_issues"]
        if i.get("severity") in ("CRITICAL", "HIGH")
    ]
    context = "\n".join(state["retrieved_context"][:3])
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
    response = invoke_llm(llm, messages, "fix_suggestion_node")
    try:
        suggestions = extract_json(response.content)
    except json.JSONDecodeError:
        suggestions = []
    return {"fix_suggestions": suggestions}
