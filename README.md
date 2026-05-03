# 🚀 GenAI Starter Workspace

Welcome to your Generative AI development hub. This workspace contains two professional-grade AI applications built using LangChain, LangGraph, and Gemini.

---

## 📂 Projects

### 1. 🛡️ Nexus Sentinel (LangGraph)
*   **Concept**: Multi-Agent Code Reviewer & Debugger.
*   **Location**: `Nexus_Sentinel/`
*   **Tech**: LangGraph (Cyclic Workflows), LangChain, Gemini 3 Flash.
*   **Feature**: It uses a specialized graph (Reviewer -> Fixer -> Verifier) to automatically detect and fix bugs in your code.

### 2. 🚀 Nexus RAG Studio (End-to-End RAG)
*   **Concept**: Professional PDF Chat Assistant.
*   **Location**: `RAG_Studio/`
*   **Tech**: Retrieval Augmented Generation (RAG), FAISS (Vector DB), LangChain 1.x.
*   **Feature**: Upload any PDF and chat with it. It uses semantic search to find facts and provides accurate answers with sources.

---

## 🛠️ Setup & Installation

1.  **Environment**: All projects share the same virtual environment located in `venv/`.
2.  **API Keys**: Ensure your `GEMINI_API_KEY` is present in the `.env` file at the root or within project folders.

---

## 🏃 How to Run

### Option A: Run All at Once (Recommended)
Double-click the **`run_all.bat`** file in the root folder.
*   **RAG Studio** will open at: `http://localhost:8501`
*   **Nexus Sentinel** will open at: `http://localhost:8502`

### Option B: Individual Run
Open a terminal in the respective project folder and run:

**For RAG Studio:**
```powershell
..\venv\Scripts\streamlit run app.py --server.port 8501
```

**For Nexus Sentinel:**
```powershell
..\venv\Scripts\streamlit run ui.py --server.port 8502
```

---

*Built with ❤️ using LangChain & Google Gemini.*
