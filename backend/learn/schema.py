from pydantic import BaseModel, Field
from typing import List

class QuizQuestion(BaseModel):
    question: str = Field(description="Quiz question text")
    options: List[str] = Field(description="List of answer options")
    correctAnswer: str = Field(description="Correct answer text")

class QuizOutput(BaseModel):
    questions: List[QuizQuestion] = Field(description="List of quiz questions")
 