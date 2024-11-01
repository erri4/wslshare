from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
@app.route('/<custom_page>')
def index(custom_page=None):
    return render_template('index.html') if custom_page is None else redirect(url_for('index'))
