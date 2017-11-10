# -*- coding: utf-8 -*-
'''信息展示接口

@author: Gao Le
'''

from flask import jsonify, request, abort, Blueprint, make_response
from model import info
from flask_jwt_extended import (create_access_token, get_jwt_identity,
                                get_jwt_claims, fresh_jwt_required,
                                set_access_cookies, unset_jwt_cookies)
from marshmallow import Schema, fields
app = Blueprint('info', __name__, url_prefix='/api')  # pylint: disable=c0103


class projectNewSchema(Schema):
    '''项目新建信息'''
    name = fields.String(required=True)
    detail = fields.String(required=False)


@app.route("/project", methods=['GET'])
@fresh_jwt_required
def project_list():
    '''获取所有项目列表

    GET /api/project
    '''
    # return make_response(jsonify(message="success", data=info.project_list(), status=200), 200)
    print("project list get")
    return jsonify(info.project_list())


@app.route("/project", methods=['POST'])
@fresh_jwt_required
def project_add():
    '''创建新项目

    POST /api/project
    '''
    if not request.json or\
        not 'name' in request.json:
        return jsonify({"msg": "Missing json in request"}), 400

    schema = projectNewSchema()
    data, errors = schema.load(request.json)
    if errors:
        return jsonify({"msg": errors}), 400
    if info.find_one_project_by_name(data["name"]):
        return jsonify({"msg": "项目名称重复"}), 200

    return jsonify(info.project_add(data)), 201


@app.route("/task", methods=['GET'])
@fresh_jwt_required
def task_list():
    '''获取所有任务列表

    GET /api/task
    '''
    # return make_response(jsonify(message="success", data=info.task_list(), status=200), 200)
    return jsonify(info.task_list())
