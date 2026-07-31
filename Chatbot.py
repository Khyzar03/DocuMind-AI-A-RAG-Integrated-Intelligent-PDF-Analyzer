# Libraries

import os
import tempfile

import streamlit as st
from dotenv import load_dotenv
from langchain_classic.chains import RetrievalQA
from langchain_classic.indexes import VectorstoreIndexCreator
from langchain_community.document_loaders import PyPDFLoader
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Page Config

st.set_page_config(
    page_title="DocuMind AI",
    page_icon="🤖",
    layout="wide",
)

# Load CSS

def load_css():
    with open("UI.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Environment

load_dotenv()


# Session State

if "messages" not in st.session_state:
    st.session_state.messages = []

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = None

# Vector Store

def get_vectorstore(_uploaded_file):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(_uploaded_file.read())
        tmp_path = tmp_file.name

    loader = PyPDFLoader(tmp_path)

    index = VectorstoreIndexCreator(
        embedding=HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        ),
        text_splitter=RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        ),
    ).from_loaders([loader])

    os.unlink(tmp_path)

    return index.vectorstore

# Header

st.markdown(
    """
<div class="main-title">
🤖 DocuMind AI
</div>

<div class="subtitle">
Chat intelligently with your PDF documents using Retrieval-Augmented Generation
</div>
""",
    unsafe_allow_html=True,
)


# Sidebar


with st.sidebar:

    st.markdown("## 📂 Documents")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    st.divider()

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []
        st.session_state.vectorstore = None
        st.session_state.uploaded_filename = None
        st.session_state.file_hash = None

        st.rerun()

    st.divider()

    st.markdown("### ⚙ Model")

    st.write("**Llama 3.1 8B Instant**")

    st.markdown("### 🧠 Embeddings")

    st.write("**MiniLM-L6-v2**")

# PDF Processing

if uploaded_file is None:

    st.markdown(
        """
<div class="glass-card">

# Welcome to DocuMind

Upload your PDF from the sidebar.

### You can ask things like:

- Summarize this document
- Explain difficult concepts
- Find important information
- Generate MCQs
- Extract key points

</div>
""",
        unsafe_allow_html=True,
    )

    st.stop()

# Build Vector Store Only If New File

if uploaded_file.name != st.session_state.uploaded_filename:

    with st.spinner("📚 Reading and indexing document..."):

        st.session_state.vectorstore = get_vectorstore(uploaded_file)

    st.session_state.uploaded_filename = uploaded_file.name

    st.session_state.messages = []

    st.success("✅ Document indexed successfully!")

vectorstore = st.session_state.vectorstore

# Suggested Questions

st.markdown("### 💡 Suggested Questions")

suggested_prompt = None

c1, c2, c3 = st.columns(3)

with c1:
    if st.button("📄 Summarize", use_container_width=True):
        suggested_prompt = "Summarize this document."

with c2:
    if st.button("📌 Key Points", use_container_width=True):
        suggested_prompt = "What are the key points of this document?"

with c3:
    if st.button("🧒 Explain Like I'm 10", use_container_width=True):
        suggested_prompt = "Explain this document in simple terms as if I were 10 years old."

st.divider()

# Chat History

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# Chat Input

user_prompt = st.chat_input("Ask anything about your document...")

prompt = suggested_prompt if suggested_prompt else user_prompt

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)

    groq_chat = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant",
    )

    try:

        with st.spinner("🤖 Thinking..."):

            qa_chain = RetrievalQA.from_chain_type(
                llm=groq_chat,
                chain_type="stuff",
                retriever=vectorstore.as_retriever(
                    search_kwargs={"k": 3}
                ),
                return_source_documents=True,
            )

            result = qa_chain({"query": prompt})

            response = result["result"]

        with st.chat_message("assistant"):

            st.markdown(response)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response,
            }
        )

    except Exception as e:

        st.error(f"Error: {e}")