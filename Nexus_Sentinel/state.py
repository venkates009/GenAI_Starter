from typing import TypedDict, List, Annotated
import operator

class AgentState(TypedDict):
    # The code we are currently working on
    code: str
    # The feedback from the reviewer
    review_feedback: List[str]
    # Results from verification
    test_results: str
    # How many times we've tried to fix it
    iteration: int
    # Final status
    status: str
