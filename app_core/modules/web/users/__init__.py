import logging

from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from app_core.utils import json_encode
from app_core.models import db, User

_logger = logging.getLogger(__name__)

user = Blueprint('user', __name__)


@user.route('/api/user/delete', methods=['POST'])
def delete_user():
    """Xoa user"""
    if request.method == 'POST':
        format_response = {
            "error": {
                "code": 0,
                "message": ""
            },
            "data": {}
        }
        data = request.get_json()
        id = data['id']
        try:
            user = User.query.filter_by(id=id).first()
            if user:
                db.session.delete(user)
                db.session.commit()
                format_response['error']['message'] = 'Xóa thành công!'
            else:
                format_response['error']['code'] = 1
                format_response['error']['message'] = 'Xóa không thành công'
            return jsonify(format_response)
        except Exception as e:
            db.session.rollback()
            return jsonify(
                {"error": {"code": 1, "message": "Internal server error!"},
                 "data": {}}), 500


@user.route('/api/user/list', methods=['GET', 'POST'])
def list_user():
    """Lấy danh sách user"""
    if request.method == 'POST':
        format_response = {
            "error": {
                "code": 0,
                "message": ""
            },
            "data": {}
        }
        data = request.get_json()
        query = User.query
        total = query.count()
        query = query.limit(data['limit']).offset(data['offset'])
        list_users = list(query)
        data_users = []
        if list_users is not None:
            for user in list_users:
                user_json = {'username':user.username,
                             'email': user.email,
                             'name': user.name}
                data_users.append(user_json)
        format_response['data'] = data_users
        format_response["total_users"] = total
        return json_encode(format_response)


@user.route('/api/user/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        format_response = {
            "error": {
                "code": 0,
                "message": ""
            },
            "data": {}
        }
        data = request.get_json()
        if data['username'] is None or data['email'] is None:
            format_response['error']['code'] = 1
            format_response['error'][
                'message'] = 'Thieu username hoac email'
            return jsonify(format_response)
        user = User.query.filter(or_(User.username.like(data['username']),
            User.email.like(data['email']))).first()
        if user:
            format_response['error']['code'] = 1
            format_response['error'][
                'message'] = 'Username hoặc email đã tồn tại'
        else:
            user = User(username=data['username'], email=data['email'],
                name=data['name'])
            db.session.add(user)
            db.session.commit()
            format_response['error']['message'] = 'Tao user thành công!'
        return jsonify(format_response)


@user.route('/api/user/modify', methods=['GET', 'POST'])
def mod_user():
    if request.method == 'POST':
        format_response = {
            "error": {
                "code": 0,
                "message": "Thành công"
            },
            "data": {}
        }
        data = request.get_json()
        user = User.query.filter_by(id=data['id']).first()
        if user:
            name = data['name']
            if len(name) != 0:
                user.name = name
                db.session.commit()
        else:
            format_response['error'] = 1
            format_response['error']['messgae'] = "Update không thành công!"

        return jsonify(format_response)
