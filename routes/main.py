from flask import render_template
from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return "Welcome to Media Downloader!"


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/docs')
def documentation():
    return render_template('documentation.html')
