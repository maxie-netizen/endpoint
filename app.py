from flask import Flask
import os
from config import Config
from extensions import db, bcrypt, login_manager   # <-- import from extensions

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Import models AFTER initializing db
    from models import User, APIKey, DownloadHistory

    # Register blueprints
    from routes.main import main
    from routes.auth import auth
    from routes.api import api
    from routes.dashboard import dashboard

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(api)
    app.register_blueprint(dashboard)

    # Create tables
    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
