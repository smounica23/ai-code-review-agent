from fastapi import APIRouter
from schemas.review_schemas import FollowUpRequest
from services.llm_client import get_llm, invoke_llm
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from agent.prompts.templates import FOLLOWUP_SYSTEM_PROMPT
import json


router = APIRouter()

@router.post("/followup")
def post_followup(request: FollowUpRequest):
    llm = get_llm()
    messages = [
        SystemMessage(content=f"""
    {FOLLOWUP_SYSTEM_PROMPT}

    The code being reviewed:
    {request.code}

    Issues found:
    {json.dumps(request.issues)}
    """)
    ]
    for msg in request.conversation_history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))
    messages.append(HumanMessage(content=request.question))
    response = invoke_llm(llm, messages, "followup")
    return {"answer": response.content}
