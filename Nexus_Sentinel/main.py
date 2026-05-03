from langgraph.graph import StateGraph, END
from state import AgentState
from agents import reviewer_node, fixer_node, verifier_node

def should_continue(state: AgentState):
    """
    Decision logic to determine the next node.
    """
    # If the verifier passed or we've reached max iterations, stop.
    if "PASSED" in state["test_results"].upper():
        return END
    
    if state["iteration"] >= 3:
        print("--- MAX ITERATIONS REACHED ---")
        return END
    
    # Otherwise, if we just fixed or verified, go back to review if failed
    if state["status"] == "verified" and "FAILED" in state["test_results"].upper():
        return "reviewer"
    
    return "fixer"

def check_review_results(state: AgentState):
    """
    Decide whether to fix or end based on review.
    """
    feedback = "".join(state["review_feedback"])
    if "NO_ISSUES" in feedback.upper() or not state["review_feedback"]:
        return END
    return "fixer"

# Initialize the Graph
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("reviewer", reviewer_node)
workflow.add_node("fixer", fixer_node)
workflow.add_node("verifier", verifier_node)

# Set Entry Point
workflow.set_entry_point("reviewer")

# Define Edges with Conditional Logic
workflow.add_conditional_edges(
    "reviewer",
    check_review_results,
    {
        "fixer": "fixer",
        END: END
    }
)

workflow.add_edge("fixer", "verifier")

workflow.add_conditional_edges(
    "verifier",
    should_continue,
    {
        "reviewer": "reviewer",
        END: END
    }
)

# Compile the Graph
app = workflow.compile()

if __name__ == "__main__":
    # Test with a buggy piece of code
    buggy_code = """
def calculate_average(numbers):
    total = sum(numbers)
    count = len(numbers)
    return total / count

# This will crash if numbers is empty
print(calculate_average([]))
    """
    
    initial_state = {
        "code": buggy_code,
        "review_feedback": [],
        "test_results": "",
        "iteration": 0,
        "status": "started"
    }
    
    print("Starting Nexus Code Sentinel...")
    final_state = app.invoke(initial_state)
    
    print("\n--- FINAL OUTPUT ---")
    print(final_state["code"])
    print(f"\nFinal Status: {final_state['status']}")
