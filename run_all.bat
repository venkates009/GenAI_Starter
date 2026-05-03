@echo off
echo 🚀 Starting GenAI Workspace Apps...

echo 🛡️ Starting Nexus Sentinel on Port 8502...
start cmd /k "cd Nexus_Sentinel && ..\venv\Scripts\streamlit run ui.py --server.port 8502"

echo 📄 Starting Nexus RAG Studio on Port 8501...
start cmd /k "cd RAG_Studio && ..\venv\Scripts\streamlit run app.py --server.port 8501"

echo ✅ Both apps are starting in separate windows.
pause
