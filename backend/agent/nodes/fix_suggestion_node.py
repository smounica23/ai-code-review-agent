from agent.state import AgentState
from services.llm_client import get_llm, invoke_llm
from agent.prompts.templates import FIX_SUGGESTION_SYSTEM_PROMPT
from langchain_core.messages import SystemMessage, HumanMessage
from services.json_utils import extract_json
import json

def fix_suggestion_node(state: AgentState) -> dict:
    print("Fix Suggestion node running...")
    llm = get_llm()

    high_issues = [
        i for i in state["security_issues"] + state["performance_issues"] + state.get("logic_issues", [])
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

    response = invoke_llm(llm, messages, "fix_suggestion_node")
    fixes = extract_json(response.content, default=[])

    all_issues = (
        state["security_issues"] +
        state["performance_issues"] +
        state["best_practice_issues"] +
        state.get("logic_issues", []) +
        state["static_issues"]
    )

    for issue in all_issues:
        for fix in fixes:
            if fix.get("rule_id") == issue.get("rule_id"):
                issue["fix_suggestion"] = fix.get("fix_code", "")
                break

    return {"all_issues": all_issues}