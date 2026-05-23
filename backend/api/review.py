from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.review_schemas import ReviewRequest, ReviewResponse
from agent.workflow import workflow
from models.db_models import CodeReview
import time, structlog

router = APIRouter()

@router.post("/review")
def post_review(request: ReviewRequest,
                db: Session = Depends(get_db)):

    review = CodeReview(
        raw_code=request.code,
        language=request.language,
        status="running"
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    initial_state = {
    "code": request.code,
    "language": request.language or "python",
    "filename": request.filename or "code",
    "review_id": review.id,
    "static_issues": [],
    "retrieved_context": [],
    "security_issues": [],
    "performance_issues": [],
    "best_practice_issues": [],
    "all_issues": [],
    "overall_score": 0.0,
    "summary": "",
    "quality_score": 0.0,
    "retry_count": 0,
    "error": None,
    "jira_ticket_id": request.jira_ticket_id,
    "jira_ticket": None,
    }
    try:
        result = workflow.invoke(initial_state)
        review.status = "complete"
        review.overall_score = result["overall_score"]
        review.summary = result["summary"]
        db.commit()
    except Exception as e:
        review.status = "failed"
        db.commit()
        raise HTTPException(status_code=500, detail=str(e))
    return {
    "review_id": review.id,
    "language": result.get("language"),
    "overall_score": result["overall_score"],
    "summary": result["summary"],
    "issues": result["all_issues"],
    "critical_count": sum(1 for i in result["all_issues"] if i.get("severity") == "CRITICAL"),
    "high_count": sum(1 for i in result["all_issues"] if i.get("severity") == "HIGH"),
    "medium_count": sum(1 for i in result["all_issues"] if i.get("severity") == "MEDIUM"),
    "low_count": sum(1 for i in result["all_issues"] if i.get("severity") == "LOW"),
    "alignment_issues": result.get("alignment_issues", []),
    "alignment_score": result.get("alignment_score", 0.0)
}