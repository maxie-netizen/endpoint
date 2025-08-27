from flask import render_template
from app import main

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/docs')
def documentation():
    return render_template('documentation.html')
