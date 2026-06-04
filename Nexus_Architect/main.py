from langgraph.graph import StateGraph, END
from state import ArchitectState
from agents import planner_node, coder_node, reviewer_node, fixer_node

def should_fix(state: ArchitectState):
    """Determine if code needs fixing or if we should end."""
    if not state["review_feedback"] or state["iteration"] >= 2:
        return END
    return "fixer"

# Initialize Graph
workflow = StateGraph(ArchitectState)

# Add Nodes
workflow.add_node("planner", planner_node)
workflow.add_node("coder", coder_node)
workflow.add_node("reviewer", reviewer_node)
workflow.add_node("fixer", fixer_node)

# Define Logic
workflow.set_entry_point("planner")
workflow.add_edge("planner", "coder")
workflow.add_edge("coder", "reviewer")

workflow.add_conditional_edges(
    "reviewer",
    should_fix,
    {
        "fixer": "fixer",
        END: END
    }
)

workflow.add_edge("fixer", "reviewer")

# Compile
app = workflow.compile()
