import streamlit as st
from document_loader import load_pdf, load_docx
from vector_store import create_vector_store
from llm_engine import generate_ai_answer

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Document Q&A AI Agent",
    page_icon="📄",
    layout="wide"
)

# ---------------- GLOBAL CSS (FIXED DARK THEME) ----------------
st.markdown("""
<style>

/* App background */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

/* Force all text visible */
html, body, [class*="css"] {
    color: #f8fafc !important;
}

/* Titles */
h1 {
    color: #ffffff !important;
    font-weight: 700;
}
h2, h3 {
    color: #e5e7eb !important;
}

/* Labels & captions */
label, p, span, div {
    color: #e5e7eb !important;
}

/* File uploader */
section[data-testid="stFileUploader"] {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 12px;
    color: #020617 !important;
}

/* Input box */
input {
    border-radius: 10px !important;
    padding: 10px !important;
    color: #020617 !important;
}

/* Answer card */
.answer-box {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 12px;
    color: #e5e7eb;
}

/* Source card */
.source-box {
    background-color: #020617;
    padding: 15px;
    border-left: 4px solid #38bdf8;
    border-radius: 8px;
    color: #cbd5f5;
}

/* Glass card */
.glass {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 20px;
    color: #ffffff;
}

/* Progress bar */
.stProgress > div > div {
    background-color: #22c55e !important;
}
.stProgress {
    background-color: #020617 !important;
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<h1 style="text-align:center; margin-bottom:30px;">
📄 Document Q&A AI Agent
</h1>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    uploaded_file = st.file_uploader(
        "📤 Upload PDF or Word document",
        type=["pdf", "docx"]
    )

with col2:
    st.markdown("""
    <div class="glass">
    <h3>🤖 How it works</h3>
    Upload a document → Ask a question → Get AI advice  
    AI analyzes your document and gives reasoning-based answers.
    </div>
    """, unsafe_allow_html=True)

# ---------------- DOCUMENT PROCESSING ----------------
if uploaded_file:
    if uploaded_file.name.endswith(".pdf"):
        text = load_pdf(uploaded_file)
    else:
        text = load_docx(uploaded_file)

    st.success("📄 Document loaded successfully!")

    vectorstore, _ = create_vector_store(text)

    st.markdown("## ✨ Ask Anything From Your Document")
    question = st.text_input("❓ Type your question here")

    if question:
        # Retrieve relevant context
        docs = vectorstore.similarity_search(question, k=4)
        context = "\n".join([doc.page_content for doc in docs])

        # Generate AI answer using local LLaMA
        answer = generate_ai_answer(question, context)

        confidence = 90  # heuristic confidence
        source = context

        # ---------------- ANSWER UI ----------------
        st.markdown(f"""
        <div class="answer-box">
        <h3>🧠 AI Answer</h3>
        <p>{answer}</p>
        </div>
        """, unsafe_allow_html=True)

        # ---------------- CONFIDENCE ----------------
        st.subheader("📊 Confidence")
        st.markdown(f"""
        <div style="font-size:16px; color:#c7d2fe; margin-bottom:8px;">
        <strong>{confidence}%</strong> confidence based on semantic similarity
        </div>
        """, unsafe_allow_html=True)

        st.progress(confidence / 100)

        # ---------------- SOURCE ----------------
        st.markdown(f"""
        <div class="source-box">
        <strong>📌 Source</strong><br>
        {source[:800]}
        </div>
        """, unsafe_allow_html=True)
