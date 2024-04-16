from flask import Flask
from .blueprints.users.user import user_bp
from .blueprints.auth.auth import auth_bp
from .blueprints.calls.call import call_bp
from flask_session import Session
from .config.local import LocalConfig
from mongoengine import connect


def create_app(config_name='local'):
    app = Flask(__name__)

    if config_name == "local":
        app.config.from_object(LocalConfig)

    connect(
        host=app.config['HOST']
    )

    # Register blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(call_bp)
    # More blueprints can be registered here

    Session(app)

    return app
