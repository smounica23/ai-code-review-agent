from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import Base, engine
from api.review import router as review_router
from api.followup import router as followup_router
from api.upload import router as upload_router
import os
from config import settings

os.environ["LANGCHAIN_TRACING_V2"] = str(settings.langchain_tracing_v2).lower()
os.environ["LANGCHAIN_API_KEY"] = settings.langchain_api_key
os.environ["LANGCHAIN_PROJECT"] = settings.langchain_project
os.environ["LANGCHAIN_ENDPOINT"] = "https://apac.api.smith.langchain.com"
@asynccontextmanager
async def lifespan(app):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="AI Code Review Agent", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def get_health():
    return {"status": "ok"}

app.include_router(review_router, prefix="/api/v1")
app.include_router(upload_router, prefix="/api/v1")
app.include_router(followup_router, prefix="/api/v1")