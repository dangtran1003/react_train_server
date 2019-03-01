# app.py
import logging
import os
import flask
import config
import logging.config

from . import models, modules

_logger = logging.getLogger(__name__)


def create_app():
    """
    Create Flask application based on env_name
    :rtype: flask.Flask
    """

    def load_app_config(app):
        """
        Load application's configurations
        :param flask.Flask app:
        :return:
        """
        instance_config_file = 'config_%s.py' % config.ENV_MODE.lower()
        app.config.from_object(config)
        app.config.from_pyfile('config.py', silent=True)
        app.config.from_pyfile(instance_config_file, silent=True)
        app.static_folder = config.STATIC_FOLDER

    app = flask.Flask(
        __name__,
        instance_relative_config=True,
        instance_path=os.path.join(config.ROOT_DIR, 'instance')
    )
    load_app_config(app)

    app.secret_key = config.SECRET_KEY

    # Sub-modules initialization
    models.init_app(app)
    modules.init_app(app)
    return app


app = create_app()
