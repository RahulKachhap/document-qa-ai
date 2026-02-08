import google.generativeai as genai
import os

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# MOST STABLE & WIDELY AVAILABLE MODEL
model = genai.GenerativeModel("models/gemini-1.0-pro")

def generate_ai_answer(question, context):
    try:
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

    except Exception as e:
        # Cloud-safe fallback (never crashes app)
        return (
            "⚠️ AI service temporarily unavailable.\n\n"
            "Please try again later or check API configuration."
        )
