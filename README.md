# 🤖 DocuMind AI

**DocuMind AI** is an intelligent document chatbot that enables users to upload PDF documents and interact with them using natural language. Powered by **Retrieval-Augmented Generation (RAG)**, it retrieves relevant information from uploaded documents and generates context-aware responses using **Groq's Llama 3.1** large language model.

Designed with a modern Streamlit interface, DocuMind AI makes it easy to summarize documents, explain complex concepts, extract key information, and answer questions with high accuracy.

---

## ✨ Features

* 📄 Upload and chat with PDF documents
* 🔍 Retrieval-Augmented Generation (RAG) for accurate responses
* 🤖 Powered by **Llama 3.1 8B Instant** via Groq API
* 🧠 Semantic search using Hugging Face embeddings
* ⚡ Fast document indexing and retrieval
* 💬 Interactive ChatGPT-style chat interface
* 💡 Suggested prompts for quick interactions
* 🎨 Modern, responsive Streamlit UI
* 🔄 Automatic document re-indexing when a new PDF is uploaded
* 🗑️ Clear chat functionality

---

## 🛠️ Tech Stack

### Frontend

* Streamlit
* Custom CSS

### Backend

* Python
* LangChain

### AI & Machine Learning

* Groq API
* Llama 3.1 8B Instant
* Hugging Face Embeddings (`all-MiniLM-L6-v2`)

### Document Processing

* PyPDFLoader
* Recursive Character Text Splitter

### Vector Store

* LangChain VectorStore

---

## 🚀 How It Works

1. Upload a PDF document.
2. The document is parsed and divided into smaller chunks.
3. Each chunk is converted into vector embeddings using Hugging Face MiniLM.
4. The embeddings are stored in a vector database.
5. When a user asks a question:

   * Relevant document chunks are retrieved.
   * Retrieved context is sent to Groq's Llama 3.1 model.
   * The model generates an accurate, context-aware response.

---

## 📸 Screenshots

<img width="1919" height="952" alt="image" src="https://github.com/user-attachments/assets/766fadd2-0bfa-4812-b826-383d809e3be7" />

<img width="1910" height="948" alt="image" src="https://github.com/user-attachments/assets/93afd995-5753-494a-94e2-dc5cac301b2d" />

---

## 👨‍💻 Author

**Khizir Junaid**

If you found this project useful, consider giving it a ⭐ on GitHub!
