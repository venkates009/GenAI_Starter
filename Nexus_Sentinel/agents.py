import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from state import AgentState

# Load environment variables (kept for other configs if needed)
load_dotenv()

# Initialize the Local LLM (Ollama)
# No API Key needed for local run!
llm = ChatOllama(model="gemma2:2b")

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
    
    prompt = f"""{system_prompt}\n\nCode to review:\n\n{code}"""
    
    response = llm.invoke(prompt)
    
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
    
    prompt = f"""{system_prompt}\n\nOriginal Code:\n{code}\n\nFeedback:\n{feedback}"""
    
    response = llm.invoke(prompt)
    
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
    
    prompt = f"""{system_prompt}\n\nCurrent Code:\n{code}"""
    
    response = llm.invoke(prompt)
    
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

def tester_node(state: AgentState):
    print("--- GENERATING UNIT TESTS ---")
    code = state["code"]
    
    system_prompt = """You are a QA Automation Engineer. Generate comprehensive Python unit tests for the provided code.
    Use the 'unittest' framework. Include:
    1. Positive test cases (normal inputs).
    2. Negative test cases (invalid inputs).
    3. Edge cases.
    
    Return ONLY the Python test code. No explanations, no markdown blocks."""
    
    prompt = f"{system_prompt}\n\nCode to test:\n{code}"
    
    response = llm.invoke(prompt)
    
    content = response.content
    if isinstance(content, list):
        result = "".join([part.get("text", "") if isinstance(part, dict) else str(part) for part in content])
    else:
        result = str(content)
        
    return {
        "test_code": result.strip(),
        "status": "testing_complete"
    }
