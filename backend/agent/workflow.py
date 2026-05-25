from langgraph.graph import START, END, StateGraph
from agent.state import AgentState
from agent.nodes.router_node import router_node
from agent.nodes.static_analysis_node import static_analysis_node
from agent.nodes.rag_retrieval_node import rag_retrieval_node
from agent.nodes.security_node import security_node
from agent.nodes.performance_node import performance_node
from agent.nodes.best_practices_node import best_practices_node
from agent.nodes.fix_suggestion_node import fix_suggestion_node
from agent.nodes.critic_node import critic_node
from agent.nodes.summary_node import summary_node
from agent.nodes.requirement_alignment_node import requirement_alignment_node
from agent.nodes.jira_fetch_node import jira_fetch_node
from agent.nodes.code_suggestion_node import code_suggestion_node

def should_retry(state: AgentState) -> str:
    if state.get("quality_score", 10) < 6 and state.get("retry_count", 0) < 2:
        return "retry"
    return "complete"

def build_workflow():

    graph = StateGraph(AgentState)
    graph.add_node("router_node", router_node)
    graph.add_node("rag_retrieval_node", rag_retrieval_node)
    graph.add_node("security_node",security_node )
    graph.add_node("static_analysis_node", static_analysis_node)
    graph.add_node("summary_node",summary_node )
    graph.add_node("best_practices_node", best_practices_node)
    graph.add_node("jira_fetch_node", jira_fetch_node)
    graph.add_node("requirement_alignment_node",requirement_alignment_node)
    graph.add_node("code_suggestion_node",code_suggestion_node)
    graph.add_node("critic_node", critic_node)
    graph.add_node("fix_suggestion_node", fix_suggestion_node)
    graph.add_node("performance_node", performance_node)
    graph.set_entry_point("router_node")

    graph.add_edge("router_node", "static_analysis_node")
    graph.add_edge("static_analysis_node", "rag_retrieval_node")
    graph.add_edge("rag_retrieval_node", "security_node")
    graph.add_edge("security_node","performance_node")
    graph.add_edge("performance_node","best_practices_node")
    graph.add_edge("best_practices_node","jira_fetch_node")
    graph.add_edge("jira_fetch_node","requirement_alignment_node")
    graph.add_edge("requirement_alignment_node","code_suggestion_node")
    graph.add_edge("code_suggestion_node","fix_suggestion_node")
    graph.add_edge("fix_suggestion_node", "critic_node")
 
    graph.add_conditional_edges("critic_node", should_retry, {
        "retry": "security_node",
        "complete": "summary_node"
    })
    graph.add_edge("summary_node", END)
    return graph.compile()

workflow = build_workflow()