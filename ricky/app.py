from flask import Flask, redirect

app = Flask(__name__)


@app.route('/')
def index():
    return redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
