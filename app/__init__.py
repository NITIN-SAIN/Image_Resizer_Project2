from flask import Flask, redirect, url_for

from config import Config
from app.extensions import db, migrate
from app.models.user import User
from app.routes.auth import auth_bp


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(auth_bp)

    @app.route("/")
    def home():
        return redirect(url_for("auth.login"))

    @app.route("/health")
    def health():
        return "OK"

    return app
