from agent.state import AgentState
from services.llm_client import get_llm, invoke_llm
from agent.prompts.templates import PERFORMANCE_SYSTEM_PROMPT
from langchain_core.messages import SystemMessage, HumanMessage
from services.json_utils import extract_json
import json

def performance_node(state:AgentState) -> dict:
    print("Performance node running...")
    llm = get_llm()
    context = "\n".join(state["retrieved_context"][:3])
    messages = [
            SystemMessage(content=PERFORMANCE_SYSTEM_PROMPT),
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
    response = invoke_llm(llm, messages, "performance_node")
    try:
        issues = extract_json(response.content)
    except json.JSONDecodeError:
        issues = []
    return {"performance_issues": issues}