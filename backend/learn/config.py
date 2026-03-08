# import google.genai as genai
# import os, sys
# from .prompt import generate_prompt

# API_KEY = os.environ["GEMINI_API_KEY"]
# MODEL = "gemini-2.5-flash-lite"
# genai.configure(api_key=API_KEY)
# client = genai.Client()
# def generate_quiz(difficulty, text):
#     response = client.models.generate_content(model=MODEL, contents=generate_prompt(difficulty=difficulty, text=text))
#     return response
import google.generativeai as genai
from .schema import QuizOutput
import os

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-2.5-flash-lite"  # or another supported model
# genai.configure(api_key=API_KEY)
client = genai.Client(api_key=API_KEY)


def generate_quiz(difficulty, text):
    prompt = generate_prompt(difficulty, text)

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config={
            # tell Gemini to produce valid JSON
            "response_mime_type": "application/json",
            # build JSON schema from Pydantic model
            "response_json_schema": QuizOutput.model_json_schema(),
        }
    )

    return QuizOutput.model_validate_json(response.text)
