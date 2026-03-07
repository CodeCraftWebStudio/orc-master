from ..general_base import db

class Quiz(db.Model):
    __tablename__ = "quizzes"

    id = db.Column(db.Integer, primary_key=True)
    difficulty = db.Column(db.String(50))

    questions = db.relationship("Question", backref="quiz", lazy=True)
                                                                                              
class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id"), nullable=False)

    question = db.Column(db.String(255), nullable=False)
    correct_answer = db.Column(db.String(128), nullable=False)

    options = db.relationship("Option", backref="question", lazy=True)


class Option(db.Model):
    __tablename__ = "options"

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)

    text = db.Column(db.String(128), nullable=False)


def return_option():
    return db.Column(db.String(128), nullable=False)

def return_question():
    return db.Column(Question(), nullable=False)