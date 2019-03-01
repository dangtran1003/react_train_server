# coding=utf-8
import logging
import flask
from flask import Blueprint

from app_core.modules.web.users import user


_logger = logging.getLogger(__name__)

web = Blueprint('sample', __name__)


def init_app(app, **kwargs):
    """
    Extension initialization point
    :param flask.Flask app:
    :param kwargs:
    :return:
    """
    app.register_blueprint(web)
    app.register_blueprint(user)
