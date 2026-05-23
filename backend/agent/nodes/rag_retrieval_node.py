from agent.state import AgentState
from rag.retriever import Retriever

retriever = Retriever()

def rag_retrieval_node(state:AgentState) -> dict:
    print("Rag Retrieval node running...")
    code = state.get("code", "")
    language = state.get("language", "")
    query = f"""
    Language : {language}
    code : {code}
    """

    chunks = retriever.retrieve(query,
                                language,
                                k=5)

    return {
        "retrieved_context": chunks
    }