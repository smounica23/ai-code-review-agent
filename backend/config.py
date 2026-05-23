from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str = ""
    groq_api_key: str = ""
    llm_provider: str = "groq"
    llm_model: str = "llama-3.3-70b-versatile"
    database_url: str ="postgresql://docuser:password@localhost:5432/code_review"
    chroma_persist_dir: str ="./chroma_db"
    langchain_api_key: str = ""
    langchain_tracing_v2: bool = False
    langchain_project: str = "ai-code-review-agent"
    langchain_endpoint: str = "https://apac.api.smith.langchain.com"
    max_code_length: int = 50000
    max_retries: int = 2
    jira_base_url: str = ""
    jira_email: str = ""
    jira_api_token: str = ""

    class Config:
        env_file=".env"

settings = Settings()