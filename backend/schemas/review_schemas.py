from typing import Optional
from pydantic import BaseModel

class ReviewRequest(BaseModel):
    code : str
    language : Optional[str] = None
    filename : Optional[str] = None
    jira_ticket_id: Optional[str] = None

class IssueResponse(BaseModel):
    category : str
    severity : str
    line_start : Optional[int]
    line_end : Optional[int]
    description : str
    fix_suggestion : Optional[str]
    rule_id : Optional[str]
    source : str

class ReviewResponse(BaseModel):

    review_id : str
    language : str
    overall_score : float
    summary : str
    issues : list[IssueResponse]
    critical_count : int
    high_count : int
    medium_count : int
    low_count : int

class FollowUpRequest(BaseModel):

    review_id : str
    question : str
    conversation_history : list[dict] = []
    code: str = ""           
    issues: list[dict] = []