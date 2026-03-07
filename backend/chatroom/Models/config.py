import os

class Config:
    SECRET_KEY = "supersecretjzhbzjx_+skxe&%"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///chat.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

