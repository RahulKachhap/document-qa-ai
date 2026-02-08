import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

def generate_ai_answer(question, context):
    prompt = f"""
You are a senior technical interviewer and career advisor.

Using the document content below:
- Analyze the question
- Give reasoning-based advice
- Suggest improvements
- Do NOT copy text verbatim

Document:
{context}

Question:
{question}

Answer professionally.
"""
    response = model.generate_content(prompt)
    return response.text
