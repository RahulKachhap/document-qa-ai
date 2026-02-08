import google.generativeai as genai
import os

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

def answer_question(question, vectorstore):
    # 1. Retrieve relevant chunks
    docs = vectorstore.similarity_search(question, k=4)
    context = "\n".join([doc.page_content for doc in docs])

    # 2. Prompt for reasoning
    prompt = f"""
You are a senior technical interviewer and career advisor.

Using the resume content below:
- Analyze role suitability
- Do NOT copy text verbatim
- Give strengths and gaps
- Suggest resume improvements

Resume Content:
{context}

User Question:
{question}

Give a clear, professional answer.
"""

    response = model.generate_content(prompt)
    answer = response.text

    # 3. Simple confidence heuristic
    confidence = min(95, 70 + len(docs) * 5)

    return answer, context, confidence
