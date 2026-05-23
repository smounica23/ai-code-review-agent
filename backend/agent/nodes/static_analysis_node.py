from agent.state import AgentState
from tools.python_tools import run_python_static_analysis
from tools.java_tools import run_java_analysis

def static_analysis_node(state:AgentState) -> dict:
    print("Static Analysis node running...")
    code = state.get("code", "")
    language = state.get("language", "")
    if language == "python":
        issues = run_python_static_analysis(code)
    elif language == "java":
        issues = run_java_analysis(code)
    else:
        issues = []

    
    return {
        "static_issues": issues
    }
