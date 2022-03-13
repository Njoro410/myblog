from flask import Flask
from config import config_options
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_materialize import Material
from flask_uploads import UploadSet, configure_uploads, IMAGES

db = SQLAlchemy()
bootstrap = Bootstrap()
material = Material()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
photos = UploadSet('photos', IMAGES)


def create_app(config_name):

    app = Flask(__name__)

    # creating app configurations
    app.config.from_object(config_options[config_name])

    # configure UploadSet
    configure_uploads(app, photos)

    # register blueprint
    from .views import views as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/authenticate')

    # initialize flask extensions
    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    material.init_app(app)

    return app
