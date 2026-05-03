import streamlit as st
from main import app
import time

st.set_page_config(page_title="Nexus Code Sentinel", layout="wide")

# Custom CSS for glassmorphism look
st.markdown("""
<style>
    .main {
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
</style>
""", unsafe_allow_html=True)

st.title("🛡️ Nexus Code Sentinel")
st.subheader("AI-Powered Multi-Agent Code Reviewer & Fixer")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📥 Input Code")
    code_input = st.text_area("Paste your buggy code here:", height=300, value="""
def get_user_data(user_id):
    # Potential SQL Injection or just bad practice
    query = "SELECT * FROM users WHERE id = " + user_id
    print(f"Executing: {query}")
    
# Passing un-sanitized input
get_user_data("1; DROP TABLE users;")
    """)
    
    start_btn = st.button("🚀 Start Sentinel Process")

with col2:
    st.markdown("### ⚙️ Sentinel Logic (LangGraph)")
    status_placeholder = st.empty()
    logs_placeholder = st.empty()

if start_btn:
    initial_state = {
        "code": code_input,
        "review_feedback": [],
        "test_results": "",
        "iteration": 0,
        "status": "started"
    }
    
    with st.spinner("Sentinel is analyzing..."):
        # We can stream the graph updates if we want, but for now, let's just run it
        # and show updates based on status
        
        # Simulating real-time updates by showing messages
        status_placeholder.info("🔍 Reviewer Node is analyzing code...")
        time.sleep(1)
        
        final_result = app.invoke(initial_state)
        
        status_placeholder.success("✅ Process Completed!")
        
        st.markdown("### 📝 Reviewer Feedback")
        for issue in final_result["review_feedback"]:
            st.warning(issue)
            
        st.markdown("### 🛠️ Fixed Code")
        st.code(final_result["code"], language="python")
        
        st.markdown(f"**Final Status:** {final_result['test_results']}")

st.sidebar.markdown("""
### About Nexus Code Sentinel
This tool uses **LangGraph** to coordinate between multiple specialized agents:
1. **Reviewer Agent**: Scans for bugs.
2. **Fixer Agent**: Generates fixes.
3. **Verifier Agent**: Confirms the fix.
""")
