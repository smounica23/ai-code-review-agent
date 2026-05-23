from sqlalchemy import Column, String, Integer, Float,DateTime,Text,ForeignKey, Enum, CheckConstraint
from database import Base
from datetime import datetime
import uuid


class CodeReview(Base):
    __tablename__ = "code_reviews"

    id = Column(String, primary_key=True, default = lambda: str(uuid.uuid4()))
    raw_code = Column(Text, nullable=False)
    language = Column(String)
    overall_score = Column(Float)
    summary = Column(Text)
    status = Column(String, default = "pending")
    created_at = Column(DateTime, default = datetime.utcnow)
    duration_seconds = Column(Float)

class ReviewIssue(Base):
    __tablename__ = "review_issues"

    id = Column(String, primary_key=True, default = lambda: str(uuid.uuid4()))
    review_id = Column(String, ForeignKey("code_reviews.id"))
    category = Column(
        Enum("security", "performance", "best_practice", name="review_category")
    )    
    severity = Column(Enum("CRITICAL", "HIGH", "MEDIUM","LOW", name="severity_level"))
    line_start = Column(Integer)
    line_end  = Column(Integer)
    description = Column(Text)
    fix_suggestion = Column(Text)
    rule_id = Column(String)
    source = Column(Enum("static_analysis", "llm", "both", name="issue_source"))

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(String, primary_key=True, default = lambda:str(uuid.uuid4()))
    review_id = Column(String, ForeignKey("code_reviews.id"))
    rating = Column(Integer)
    __table_args__ = (
        CheckConstraint("rating >= 1 AND rating <= 5", name="check_rating_1_to_5"),
    )
    comment = Column(Text)
    created_at = Column(DateTime, default = datetime.utcnow)
