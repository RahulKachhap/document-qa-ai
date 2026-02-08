import subprocess

def generate_ai_answer(question, context):
    prompt = f"""
You are a senior technical interviewer and career advisor.

Using the resume content below:
- Decide if the candidate fits the role
- Explain strengths
- Identify gaps
- Suggest resume improvements
- Do NOT copy text directly

Resume Content:
{context}

User Question:
{question}

Give a professional, helpful answer.
"""

    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt,
        text=True,
        capture_output=True
    )

    return result.stdout.strip()
