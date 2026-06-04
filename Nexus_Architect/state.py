from typing import TypedDict, List

class ArchitectState(TypedDict):
    task_description: str
    plan: str
    code: str
    review_feedback: List[str]
    iteration: int
    status: str
