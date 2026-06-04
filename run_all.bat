@echo off
echo 🚀 Starting GenAI Workspace Apps with Local Ollama...

:: Setting the environment variable for Ollama models on D: drive
set OLLAMA_MODELS=D:\Ollama_Models

echo 🏗️ Starting Nexus Architect on Port 8503...
start cmd /k "cd Nexus_Architect && set OLLAMA_MODELS=D:\Ollama_Models && ..\venv\Scripts\streamlit run ui.py --server.port 8503"

echo 🛡️ Starting Nexus Sentinel on Port 8502...
start cmd /k "cd Nexus_Sentinel && set OLLAMA_MODELS=D:\Ollama_Models && ..\venv\Scripts\streamlit run ui.py --server.port 8502"

echo 📄 Starting Nexus RAG Studio on Port 8501...
start cmd /k "cd RAG_Studio && set OLLAMA_MODELS=D:\Ollama_Models && ..\venv\Scripts\streamlit run app.py --server.port 8501"

echo ✅ All 3 apps are starting in separate windows using Local LLMs.
pause
