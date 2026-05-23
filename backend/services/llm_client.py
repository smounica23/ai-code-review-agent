from langchain_groq import ChatGroq
from config import settings

def get_llm(temperature: float = 0.1) :
    return ChatGroq(
        model= settings.llm_model,
        temperature = temperature,
        groq_api_key=settings.groq_api_key
    )

def invoke_llm(llm, messages, agent_name:str):
    response = llm.invoke(messages)
    print(f"[{agent_name}] input_tokens: {response.usage_metadata.get('input_tokens', 0)} output_tokens: {response.usage_metadata.get('output_tokens', 0)}")    
    return response