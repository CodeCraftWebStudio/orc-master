from flask import Flask, jsonify, redirect, request
from flask_cors import CORS

app = Flask(__name__)
CORS(
    app,
    supports_credentials=True,
    origins=["http://localhost:*", "http://127.0.0.1:*"]
)
