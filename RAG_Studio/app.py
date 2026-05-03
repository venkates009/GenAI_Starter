import streamlit as st
import os
from dotenv import load_dotenv

# LangChain Imports
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

# 1. Configuration
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="Nexus RAG Studio", layout="wide")

# Custom CSS for a clean, sweet light theme
st.markdown("""
<style>
    /* Light background with a soft tint */
    .stApp {
        background-color: #f8fafc;
        color: #1e293b;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Professional Headers */
    h1, h2, h3 {
        color: #0f172a !important;
        font-weight: 700 !important;
    }

    /* Buttons with a sweet sky-blue gradient */
    .stButton>button {
        background: linear-gradient(90deg, #0ea5e9 0%, #38bdf8 100%);
        color: white;
        border: none;
        padding: 0.6rem 1rem;
        border-radius: 12px;
        font-weight: 600;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 15px -3px rgba(14, 165, 233, 0.3);
    }
    
    /* Chat message cards */
    .stChatMessage {
        background-color: #ffffff !important;
        border-radius: 15px;
        margin-bottom: 12px;
        border: 1px solid #f1f5f9;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    
    /* Input field styling */
    .stChatInputContainer {
        border-radius: 15px;
    }
</style>
""", unsafe_allow_html=True)

# 2. Core RAG Logic Functions
def process_pdf(file_path):
    """Extracts text from PDF and splits it into chunks."""
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    # Chunking: 1000 characters per chunk with 200 character overlap
    # Overlap helps maintain context between chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    return chunks

def create_vector_db(chunks):
    """Converts text chunks into embeddings and saves them in FAISS."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vector_db = FAISS.from_documents(chunks, embeddings)
    return vector_db

def get_rag_chain(vector_db):
    """Creates a RetrievalQA chain using Gemini."""
    llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0.3)
    
    # Custom Prompt Template
    template = """You are a professional research assistant. Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Keep the answer concise and professional.

    Context: {context}
    Question: {question}

    Helpful Answer:"""
    
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)
    
    # Combine everything into a chain
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_db.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )
    return chain

# 3. Streamlit UI
st.title("🛡️ Nexus RAG Studio")
st.subheader("Professional PDF Chat Assistant")

# Sidebar for Uploads
with st.sidebar:
    st.header("Document Center")
    uploaded_file = st.file_uploader("Upload your PDF", type="pdf")
    
    if uploaded_file:
        # Save temp file
        temp_path = "temp_doc.pdf"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        if st.button("Index Document"):
            with st.spinner("Processing & Embedding..."):
                chunks = process_pdf(temp_path)
                vector_db = create_vector_db(chunks)
                st.session_state.vector_db = vector_db
                st.success("Indexing Complete!")

# Main Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if query := st.chat_input("Ask a question about the document..."):
    if "vector_db" not in st.session_state:
        st.error("Please upload and index a document first!")
    else:
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)
            
        # Generate Answer
        with st.chat_message("assistant"):
            with st.spinner("Searching document..."):
                chain = get_rag_chain(st.session_state.vector_db)
                response = chain({"query": query})
                answer = response["result"]
                st.markdown(answer)
                
                # Show sources (Optional but professional)
                with st.expander("View Sources"):
                    for doc in response["source_documents"]:
                        st.write(f"- {doc.page_content[:200]}...")
                
                st.session_state.messages.append({"role": "assistant", "content": answer})
