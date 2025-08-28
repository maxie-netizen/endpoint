from flask import Flask
from config import Config
from extensions import db, bcrypt, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    # Import models after db is initialized
    from models import User, APIKey, DownloadHistory

    # Create tables
    with app.app_context():
        db.create_all()

    # Import routes
    from routes import main, auth, api, dashboard

    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(api)
    app.register_blueprint(dashboard)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
