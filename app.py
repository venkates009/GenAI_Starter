import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from pypdf import PdfReader

# 1. Page Configuration
st.set_page_config(page_title="AI Document Studio", page_icon="📄")

# 2. Load API Key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("❌ API Key missing!")
    st.stop()

client = genai.Client(api_key=API_KEY)

# 3. Sidebar for PDF Upload
with st.sidebar:
    st.title("📄 PDF Upload")
    uploaded_file = st.file_uploader("Upload a PDF file to chat with it", type="pdf")
    
    pdf_text = ""
    if uploaded_file:
        with st.spinner("Extracting text from PDF..."):
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                pdf_text += page.extract_text()
        st.success("PDF loaded successfully!")
        st.info(f"PDF length: {len(pdf_text)} characters")

    st.markdown("---")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# 4. Main UI
st.title("📄 Chat with your PDF")
st.write("Upload a document in the sidebar and ask questions about it.")
st.markdown("---")

# 5. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 6. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. Chat Input and AI Logic
if prompt := st.chat_input("Ask me anything about the PDF..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Analyzing document... 🔍")
        
        try:
            # Building the context
            # If a PDF is uploaded, we prepend its content to the prompt
            context = f"Context from uploaded PDF:\n{pdf_text}\n\nUser Question: {prompt}" if pdf_text else prompt
            
            # Create the message list for history
            # Note: For simplicity, we only send the context with the latest message
            # but keep the history structure
            history = []
            for m in st.session_state.messages[:-1]:
                history.append({"role": m["role"], "parts": [{"text": m["content"]}]})
            
            # The latest message has the context
            history.append({"role": "user", "parts": [{"text": context}]})

            response = client.models.generate_content(
                model='gemini-flash-latest',
                contents=history
            )
            
            full_response = response.text
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error: {e}")
