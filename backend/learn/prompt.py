def generate_prompt(difficulty, text):
    prompt = f"""
You are an educational content generator.

Generate 30 multiple-choice quiz questions.

Rules:
- Difficulty level: {difficulty}
- Base questions primarily on the provided text
- Do NOT invent specific facts not implied by the text
- Return ONLY valid JSON
- No markdown, no explanations

JSON format:
{
  "questions": [
    {
      "question": "",
      "options": ["", "", "", "", ""],
      "correctAnswer": ""
    }
  ]
}

TEXT:
<<<
{text}
>>>
"""
    return prompt