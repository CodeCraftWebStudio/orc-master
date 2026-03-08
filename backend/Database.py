from flask import Flask, jsonify, redirect, request
from flask_cors import CORS

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

CORS(
    app,
    supports_credentials=True,
    origins=[
        "http://localhost:*",
        "http://127.0.0.1:*",
        "https://boisterous-alfajores-6bcd79.netlify.app"
    ]
)
