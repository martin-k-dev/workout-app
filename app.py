from flask import Flask
from parser import clear_data, read_example_files

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p><h3>URL example (for one session): http://127.0.0.1:5000/api/2026-01-01</h3>"

@app.route("/api/")
def show_basic_api():
    return clear_data(read_example_files())

@app.route("/api/<date>")
def get_one_workout(date):
    data: dict = clear_data(read_example_files())
    return data[date]
