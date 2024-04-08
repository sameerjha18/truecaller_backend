from flask import Flask
from .blueprints.users.user import user_bp
from .blueprints.auth.auth import auth_bp
from .blueprints.calls.call import call_bp
from api.models.model import db
from flask_session import Session
from .config.local import LocalConfig
    


def create_app(config_name='local'):
    app = Flask(__name__)

    if config_name == "local":    
        app.config.from_object(LocalConfig)

    db.init_app(app)

    # Register blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(call_bp)
    # More blueprints can be registered here
    with app.app_context():
        db.create_all()

    Session(app)

    return app