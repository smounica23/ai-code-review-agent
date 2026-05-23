from agent.state import AgentState
from services.llm_client import get_llm, invoke_llm
from agent.prompts.templates import SECURITY_SYSTEM_PROMPT
from langchain_core.messages import SystemMessage, HumanMessage
from services.json_utils import extract_json
import json

def security_node(state: AgentState) -> dict:
    print("Security node running...")
    llm = get_llm()
    
    context = "\n".join(state["retrieved_context"][:3])
    
    messages = [
        SystemMessage(content=SECURITY_SYSTEM_PROMPT),
        HumanMessage(content=f"""
Language: {state["language"]}
Static analysis findings: {json.dumps(state["static_issues"])}
Relevant security guidelines: {context}

Code to review:
```{state["language"]}
{state["code"]}
```

Return ONLY a JSON array.
""")
    ]
    
    response = invoke_llm(llm, messages, "security_node")
    
    try:
        issues = extract_json(response.content)
    except json.JSONDecodeError:
        issues = []
    
    return {"security_issues": issues}