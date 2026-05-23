# 🔍 AI Code Review Agent

An intelligent, multi-agent code review system that analyzes source code for security vulnerabilities, performance issues, and best practices — and checks whether the code actually implements the requirements from your Jira ticket.

Built with LangGraph, FastAPI, RAG, and real static analysis tools.

---

## 🎯 What Makes This Different

| Feature | This Agent | Traditional CI/CD | ChatGPT |
|---|---|---|---|
| Static analysis tools | ✅ ruff, bandit | ✅ | ❌ |
| Semantic understanding | ✅ LLM agents | ❌ | ✅ |
| Jira requirement check | ✅ | ❌ | ❌ |
| Fix suggestions | ✅ | ❌ | ✅ |
| RAG-grounded findings | ✅ | ❌ | ❌ |
| Self-correction loop | ✅ critic agent | ❌ | ❌ |
| Line-level comments | ✅ | ✅ | ❌ |
| Follow-up Q&A | ✅ | ❌ | ✅ |
| LangSmith observability | ✅ | ❌ | ❌ |
| GitHub Actions CI/CD | ✅ | ✅ | ❌ |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     STREAMLIT FRONTEND                      │
│   [Upload/Paste Code] → [Jira Ticket ID] → [Run Review]    │
│   [Issue Cards] [Severity] [Line #] [Fix] [Follow-up Q&A]  │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTP REST
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   FASTAPI BACKEND                           │
│   POST /review  │  POST /upload  │  POST /followup          │
└──────┬──────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│               LANGGRAPH AGENT WORKFLOW (10 nodes)           │
│                                                             │
│  [Router] → [Static Analysis] → [RAG Retrieval]            │
│       ↓              ↓                  ↓                   │
│  [Security]    [Performance]    [Best Practices]            │
│       └──────────────┴────────────────┘                     │
│                       ↓                                     │
│              [Jira Fetch] → [Requirement Alignment]         │
│                       ↓                                     │
│              [Fix Suggestion Agent]                         │
│                       ↓                                     │
│              [Critic / Evaluator] ←── self-correction loop  │
│                       ↓                                     │
│              [Summary Agent] → Final JSON Response          │
└──────┬───────────────────────┬──────────────────────────────┘
       │                       │
       ▼                       ▼
┌──────────────┐    ┌──────────────────────────────────────────┐
│  STATIC      │    │              RAG KNOWLEDGE BASE           │
│  ANALYZERS   │    │  ChromaDB + sentence-transformers         │
│  ruff        │    │  OWASP Top 10                            │
│  bandit      │    │  Python/Java best practices              │
│  java rules  │    │  Secure coding guidelines                │
└──────────────┘    └──────────────────────────────────────────┘
                                │
                    ┌───────────▼──────────────┐
                    │   JIRA REST API           │
                    │   Fetch ticket details    │
                    │   Extract AC + description│
                    └──────────────────────────┘
```

---

## 🤖 Agent Workflow

The system uses **10 specialized agents** orchestrated by LangGraph:

| Agent | Responsibility |
|---|---|
| Router | Detect language, validate input |
| Static Analysis | Run ruff + bandit as subprocesses |
| RAG Retrieval | Fetch relevant guidelines from ChromaDB |
| Security | Find OWASP vulnerabilities |
| Performance | Find runtime bottlenecks |
| Best Practices | Find code quality issues |
| Jira Fetch | Retrieve ticket from Jira REST API |
| Requirement Alignment | Check code vs acceptance criteria |
| Fix Suggestion | Generate copy-pasteable code fixes |
| Critic | Validate review quality — self-correction loop |
| Summary | Synthesize final structured report |

---

## 🛠️ Tech Stack

- **Agent Framework:** LangGraph (StateGraph, conditional edges)
- **LLM:** Groq (llama-3.3-70b-versatile)
- **Backend:** FastAPI + SQLAlchemy + PostgreSQL
- **Frontend:** Streamlit
- **RAG:** ChromaDB + sentence-transformers (all-MiniLM-L6-v2)
- **Static Analysis:** ruff, bandit (Python) + regex rules (Java)
- **Observability:** LangSmith (zero-code tracing)
- **Integration:** Jira REST API
- **CI/CD:** GitHub Actions
- **Containerization:** Docker + docker-compose

---

## 🚀 Quickstart

**1. Clone the repo**
```bash
git clone https://github.com/smounica23/ai-code-review-agent.git
cd ai-code-review-agent
```

**2. Set up environment**
```bash
cd backend
python -m venv venv
source venv/Scripts/activate  # Windows
pip install -r requirements.txt
```

**3. Configure environment variables**
```bash
cp .env.example backend/.env
# edit backend/.env with your API keys
```

**4. Ingest knowledge base**
```bash
python -m rag.ingest
```

**5. Run the backend**
```bash
uvicorn main:app --reload --port 8000
```

**6. Run the frontend**
```bash
cd frontend
streamlit run app.py
```

Open `http://localhost:8501`

---

## 📡 API Endpoints

**Review code:**
```bash
curl -X POST http://localhost:8000/api/v1/review \
  -H "Content-Type: application/json" \
  -d '{
    "code": "import pickle\npassword = \"admin123\"",
    "language": "python",
    "jira_ticket_id": "KAN-4"
  }'
```

**Ask follow-up question:**
```bash
curl -X POST http://localhost:8000/api/v1/followup \
  -H "Content-Type: application/json" \
  -d '{
    "review_id": "your-review-id",
    "question": "Why is pickle dangerous?",
    "conversation_history": []
  }'
```

**Health check:**
```bash
curl http://localhost:8000/health
```

---

## 🔁 GitHub Actions CI/CD

Every PR automatically triggers the agent:

1. Extracts Jira ticket ID from PR title (e.g. `[KAN-4] Add login endpoint`)
2. Reviews all changed `.py`, `.java`, `.js` files
3. Posts structured comment with findings
4. **Blocks merge if critical issues found**

Required GitHub secret: `REVIEW_API_URL`

---

## 📊 Observability

LangSmith provides zero-code tracing:
- Every agent node execution
- Token usage per LLM call
- Latency per node
- Full input/output visibility

Set `LANGCHAIN_TRACING_V2=true` in `.env` — no other code changes needed.

---

## 🗂️ Project Structure

```
ai-code-review-agent/
├── backend/
│   ├── agent/
│   │   ├── nodes/          # 10 specialized agent nodes
│   │   ├── prompts/        # System prompts for each agent
│   │   ├── state.py        # LangGraph AgentState TypedDict
│   │   └── workflow.py     # StateGraph definition
│   ├── api/                # FastAPI endpoints
│   ├── rag/                # ChromaDB ingestion + retriever
│   ├── tools/              # Static analysis + Jira tools
│   ├── services/           # LLM client + JSON utils
│   └── models/             # SQLAlchemy models
├── frontend/
│   └── app.py              # Streamlit UI
├── scripts/
│   └── github_review.py    # GitHub Actions review script
├── .github/
│   └── workflows/
│       └── code_review.yml # GitHub Actions workflow
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 📝 Environment Variables

See `.env.example` for all required variables:

```
GROQ_API_KEY          # Groq LLM API key
DATABASE_URL          # PostgreSQL connection string
LANGCHAIN_API_KEY     # LangSmith observability
JIRA_BASE_URL         # Your Jira domain
JIRA_EMAIL            # Your Jira email
JIRA_API_TOKEN        # Jira API token
```