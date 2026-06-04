import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from state import ArchitectState

# Load environment variables
load_dotenv()

# Initialize the Local LLM (Ollama) - Completely Free
llm = ChatOllama(model="gemma2:2b")

def planner_node(state: ArchitectState):
    print("--- PLANNING TASK ---")
    task = state["task_description"]
    
    prompt = f"""You are a Software Architect. Break down the following request into a logical step-by-step coding plan.
    Request: {task}
    
    Return ONLY the plan as a concise bulleted list."""
    
    response = llm.invoke(prompt)
    return {"plan": response.content, "status": "planned"}

def coder_node(state: ArchitectState):
    print("--- WRITING CODE ---")
    task = state["task_description"]
    plan = state["plan"]
    
    prompt = f"""You are a Senior Python Developer. Write a complete, working Python script based on the following plan.
    Task: {task}
    Plan: {plan}
    
    Return ONLY the code. No explanations, no markdown blocks."""
    
    response = llm.invoke(prompt)
    return {"code": response.content, "status": "coded"}

def reviewer_node(state: ArchitectState):
    print("--- AUDITING GENERATED CODE ---")
    code = state["code"]
    
    prompt = f"""You are a Security & Logic Auditor. Review the following code for bugs, security issues, or inefficiencies.
    Code: {code}
    
    If perfect, respond with 'NO_ISSUES'. Otherwise, list the issues concisely."""
    
    response = llm.invoke(prompt)
    feedback = response.content
    return {"review_feedback": [feedback] if "NO_ISSUES" not in feedback else [], "status": "reviewed"}

def fixer_node(state: ArchitectState):
    print("--- REFINING CODE ---")
    code = state["code"]
    feedback = "".join(state["review_feedback"])
    
    prompt = f"""You are a Fixer Agent. Improve the following code based on this feedback:
    Feedback: {feedback}
    Original Code: {code}
    
    Return ONLY the corrected, perfect code. No markdown."""
    
    response = llm.invoke(prompt)
    return {"code": response.content, "iteration": state["iteration"] + 1, "status": "refined"}
