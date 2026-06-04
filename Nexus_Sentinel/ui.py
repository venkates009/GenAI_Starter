import streamlit as st
from main import app
import time

st.set_page_config(page_title="Nexus Code Sentinel", layout="wide")

# Custom CSS for glassmorphism look
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
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .stTabs [data-baseweb="tab"] {
        color: #94a3b8;
    }
    .stTabs [aria-selected="true"] {
        color: #ffffff;
        border-bottom-color: #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ Nexus Code Sentinel")
st.subheader("Multi-Agent Project Auditor")

# Sidebar for File Uploads
with st.sidebar:
    st.header("Project Files")
    uploaded_files = st.file_uploader("Upload Python files for review", type="py", accept_multiple_files=True)
    
    start_btn = st.button("🚀 Analyze All Files")
    
    st.markdown("---")
    st.markdown("""
    ### About Nexus Code Sentinel
    This tool uses **LangGraph** to coordinate between:
    1. **Reviewer Agent**: Scans for bugs.
    2. **Fixer Agent**: Generates fixes.
    3. **Verifier Agent**: Confirms the fix.
    """)

# Session state to store results
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = {}

if start_btn and uploaded_files:
    # Clear previous results
    st.session_state.analysis_results = {}
    
    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name
        code_content = uploaded_file.getvalue().decode("utf-8")
        
        with st.spinner(f"Sentinel analyzing {file_name}..."):
            initial_state = {
                "code": code_content,
                "review_feedback": [],
                "test_results": "",
                "iteration": 0,
                "status": "started"
            }
            
            # Run the graph
            final_result = app.invoke(initial_state)
            st.session_state.analysis_results[file_name] = final_result
            
    st.success("Batch Analysis Complete!")

# Display Results
if st.session_state.analysis_results:
    st.markdown("### 📊 Analysis Results")
    file_tabs = st.tabs(list(st.session_state.analysis_results.keys()))
    
    for i, (file_name, result) in enumerate(st.session_state.analysis_results.items()):
        with file_tabs[i]:
            st.subheader(f"Results for {file_name}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 🛠️ Fixed Code")
                st.code(result['code'], language='python')
                
                st.markdown("#### 🧪 Generated Unit Tests")
                st.code(result.get('test_code', '# No tests generated'), language='python')
            
            with col2:
                st.markdown("#### 📝 Agent Feedback")
                if result["review_feedback"]:
                    for issue in result["review_feedback"]:
                        st.warning(issue)
                else:
                    st.success("No issues found in this file!")
                
                st.markdown(f"**Final Status:** {result['test_results']}")
else:
    st.info("👈 Upload your Python files in the sidebar and click 'Analyze All Files' to start the audit.")
