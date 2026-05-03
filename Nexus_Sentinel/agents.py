import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from state import AgentState

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Initialize the LLM
# LangGraph nodes are just functions that take 'state' and return 'updates to state'
llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", google_api_key=api_key)

def reviewer_node(state: AgentState):
    print("--- REVIEWING CODE ---")
    code = state["code"]
    
    system_prompt = """You are an expert Senior Software Engineer. 
    Review the provided code for:
    1. Logical bugs
    2. Efficiency issues
    3. Security vulnerabilities
    4. Best practices
    
    Provide a concise list of issues found. If the code is perfect, say 'NO_ISSUES'."""
    
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Code to review:\n\n{code}")
    ])
    
    # Handle cases where response.content might be a list
    content = response.content
    if isinstance(content, list):
        feedback = "".join([part.get("text", "") if isinstance(part, dict) else str(part) for part in content])
    else:
        feedback = str(content)
        
    feedback = feedback.strip()
    issues = [f.strip() for f in feedback.split('\n') if f.strip()]
    
    return {
        "review_feedback": issues,
        "status": "reviewed"
    }

def fixer_node(state: AgentState):
    print("--- FIXING CODE ---")
    code = state["code"]
    feedback = "\n".join(state["review_feedback"])
    
    system_prompt = """You are an expert Coder. 
    Fix the code based on the feedback provided. 
    Return ONLY the corrected code. No explanations, no markdown blocks."""
    
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Original Code:\n{code}\n\nFeedback:\n{feedback}")
    ])
    
    # Handle cases where response.content might be a list
    content = response.content
    if isinstance(content, list):
        new_code = "".join([part.get("text", "") if isinstance(part, dict) else str(part) for part in content])
    else:
        new_code = str(content)
    
    # Clean up the output in case LLM adds markdown
    new_code = new_code.replace("```python", "").replace("```", "").strip()
    
    return {
        "code": new_code,
        "iteration": state["iteration"] + 1,
        "status": "fixed"
    }

def verifier_node(state: AgentState):
    print("--- VERIFYING FIX ---")
    code = state["code"]
    original_feedback = "\n".join(state["review_feedback"])
    
    system_prompt = """You are a QA Engineer. 
    Check if the new code has resolved the issues previously identified.
    Feedback was: {feedback}
    
    If resolved, respond with 'PASSED'.
    If issues still exist or new ones appeared, respond with 'FAILED' and explain why.""".format(feedback=original_feedback)
    
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Current Code:\n{code}")
    ])
    
    # Handle cases where response.content might be a list
    content = response.content
    if isinstance(content, list):
        result = "".join([part.get("text", "") if isinstance(part, dict) else str(part) for part in content])
    else:
        result = str(content)
    
    result = result.strip()
    
    return {
        "test_results": result,
        "status": "verified"
    }
