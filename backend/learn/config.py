import os
import google.generativeai as genai
from .schema import QuizOutput
from .prompt import generate_prompt

# Get API key from environment
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=API_KEY)

# Model to use
MODEL = "gemini-1.5-flash"


def generate_quiz(difficulty, text):
    prompt = generate_prompt(difficulty, text)

    model = genai.GenerativeModel(MODEL)

    response = model.generate_content(
        prompt,
        generation_config={
            "response_mime_type": "application/json",
        },
    )

    # Parse JSON response into Pydantic model
    return QuizOutput.model_validate_json(response.text)
