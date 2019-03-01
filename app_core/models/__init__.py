# coding=utf-8
import logging

import flask_migrate
import flask_sqlalchemy as _fs

_logger = logging.getLogger(__name__)

db = _fs.SQLAlchemy()
migrate = flask_migrate.Migrate(db=db)


def init_app(app, **kwargs):
    """
    Extension initialization point
    :param flask.Flask app:
    :param kwargs:
    :return:
    """
    db.app = app
    db.init_app(app)
    migrate.init_app(app)

    _logger.info('Start app with database: %s' %
                 app.config['SQLALCHEMY_DATABASE_URI'])

from .base_model import BaseModel
from .user import User
