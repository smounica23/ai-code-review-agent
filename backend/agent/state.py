from typing import TypedDict, Optional

class AgentState(TypedDict) :
    code : str
    language : str
    filename : str
    review_id : str
    static_issues : list
    retrieved_context  : list
    security_issues : list
    performance_issues  : list
    best_practice_issues : list
    all_issues : list
    retry_count : int
    overall_score: float
    summary: str
    quality_score: float
    error: Optional[str]
    jira_ticket_id: Optional[str]
    jira_ticket: Optional[dict]
    alignment_issues: list
    alignment_score: float
    code_suggestions: list
    logic_issues: list
