import streamlit as st
from main import app

st.set_page_config(page_title="Nexus Architect", layout="wide")

# Premium Dark Glassmorphism CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white;
    }
    .stTextArea textarea {
        background-color: #1e293b !important;
        color: #e2e8f0 !important;
        border: 1px solid #334155 !important;
    }
    .stButton>button {
        background: linear-gradient(90deg, #8b5cf6 0%, #7c3aed 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(139, 92, 246, 0.4);
    }
    .stCodeBlock {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏗️ Nexus Architect")
st.subheader("Autonomous Local Code Generator")

# Input Area
st.markdown("### 💡 What do you want to build?")
task_input = st.text_area("Describe your project or function:", height=150, placeholder="Example: Create a Python script that scrapes news from a website and saves it to a CSV file.")

if st.button("🚀 Generate Project"):
    if not task_input.strip():
        st.warning("Please describe the task first!")
    else:
        with st.spinner("Architect is planning and writing..."):
            initial_state = {
                "task_description": task_input,
                "plan": "",
                "code": "",
                "review_feedback": [],
                "iteration": 0,
                "status": "started"
            }
            
            final_result = app.invoke(initial_state)
            
            st.success("Generation Complete!")
            
            # Display Layout
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("### 📋 The Plan")
                st.info(final_result["plan"])
                
                with st.expander("View Audit Feedback"):
                    if final_result["review_feedback"]:
                        for f in final_result["review_feedback"]:
                            st.warning(f)
                    else:
                        st.success("Code passed all security & logic audits!")

            with col2:
                st.markdown("### 🛠️ Generated Code")
                st.code(final_result["code"], language="python")
                
                st.download_button(
                    label="📥 Download Code",
                    data=final_result["code"],
                    file_name="generated_project.py",
                    mime="text/x-python"
                )

st.sidebar.markdown("""
---
### How it works
1. **Local LLM**: Uses Gemma 2 (2B) on your machine.
2. **Multi-Agent**: Planner writes the steps, Coder writes the code.
3. **Built-in Sentinel**: Automatically reviews and fixes the code before showing it to you.
---
**100% Free & Quota-free.**
""")
