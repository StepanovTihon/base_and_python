import json
import random

import time
from BaseWorkspace import *
from AddedFunctions import *

from flask import Flask, request

# from dotenv import load_dotenv

try:
    create_apartments("testaddress2")
except BaseError as be:
    print(be.txt)

# load_dotenv()
app = Flask(__name__)


@app.route('/info/<int:id>/<int:token>')
def get_lodgers(id, token):
    post = read_lodgers(id)
    print(read_token(id)[0], token)
    if read_token(id)[0] != token:
        return '{"error":"token is deprecated"}', 401
    if len(post[0]) == 0:
        return errors[post[1]], 400
    return json.dumps(to_json(["name_lodgers", "lodgers_id", "login", "password", "token"], post)), 200


@app.route('/AllLodger/')
def get_all_lodgers():
    post = read_all_lodgers()

    post_json = {}
    to_json_keys = ['name_lodgers', 'lodgers_id', 'login', 'password', 'token']

    return mass_to_json(to_json_keys, post)


@app.route('/registration/', methods=['POST'])
def registration():
    post = request.json
    ret = create_lodgers(post["name"], post["login"], post["password"])

    return "{}", 200


@app.route('/login', methods=['POST'])
def login():
    post = request.json
    ret = read_all_lodgers()
    if len(ret[0]) == 0:
        time.sleep(15)
        return errors[ret[1]], 400

    for i in range(len(ret[0])):
        print(ret[0][i][0])
        if ret[0][i][2] == post["login"] and ret[0][i][3] == post["password"]:
            return '{"token":"' + str(ret[0][i][4]) + '", "lodgers_id":' + str(ret[0][i][1]) + '}', 200

    time.sleep(15)
    return '{"error":"Bad request"}', 400


# @app.route('/delete_lodger/', methods=['POST'])
# def delete_lodger():
#     post = request.json
#     if read_token(post["id"]) != post["token"]:
#         return "{'error':'token is deprecated'}"
#     ret = delete_lodger(post["id"])
#
#     return "{'error':'Deleted'}"


@app.route('/create_home/', methods=['POST'])
def create_home():
    post = request.json
    ret = create_apartments(post["address"])

    return "{}", 200


# @app.route('/get_home/<int:id>/<int:token>')
# def get_home(id, token):
#     post = read_all_apartments()
#     if read_token(id) != token:
#         return "{'error':'token is deprecated'}"
#
#     to_json_keys = ['apartments_id', 'address']
#     post_json = {}
#     resilt_json = "["
#
#     for i in range(len(post)):
#         for index, value in enumerate(post[i]):
#             post_json[to_json_keys[index]] = value
#
#         resilt_json += json.dumps(post_json) + ", "
#         post_json.clear()
#
#     resilt_json = resilt_json[:len(resilt_json) - 2] + "]"
#     return resilt_json


# @app.route('/delete_home/', methods=['POST'])
# def delete_home():
#     post = request.json
#     if read_token(post["id"]) != post["token"]:
#         return "{'error':'token is deprecated'}"
#     ret = delete_apartments(post["apartments_id"])
#
#     return "{'error':'Deleted'}"


@app.route('/create_service/', methods=['POST'])
def create_service():
    post = request.json
    if int(read_token(post["lodgers_id"])[0]) != int(post["token"]):
        return "{'error':'token is deprecated'}", 400
    ret = create_services(post["services_name"], post["payment_amount"], post["apartments_id"], post["lodgers_id"],
                          post["date_services"])

    return "{}", 200


@app.route('/create_indication/', methods=['POST'])
def create_indication():
    post = request.json

    if int(read_token(post["lodgers_id"])[0]) != int(post["token"]):
        return "{'error':'token is deprecated'}", 400

    ret = create_indications(post["services_name"], post["apartments_id"], post["lodgers_id"], post["date_indications"],
                             post["value_indications"])
    return "{}", 200


@app.route('/get_indication/<int:id>/<int:token>')
def get_indication(id, token):
    post = read_indications(id)
    print(read_token(id)[0], token)
    if int(read_token(id)[0]) != int(token):
        return '{"error":"token is deprecated"}'

    to_json_keys = ["indications_id", "services_name", "apartments_id", "lodgers_id", "date_indications",
                    "value_indications"]

    return mass_to_json(to_json_keys, post)


@app.route('/get_service/<int:id>/<int:token>')
def get_service(id, token):
    post = read_services(id)
    print(read_token(id)[0], token)
    if read_token(id)[0] != token:
        return '{"error":"token is deprecated"}'

    to_json_keys = ['services_name', 'payment_amount', 'date_services', 'paid', 'name_lodgers', 'lodgers_id', 'address',
                    'apartments_id']
    post_json = {}

    return mass_to_json(to_json_keys, post)


# @app.route('/get_all_service/<int:id>/<int:token>')
# def get_all_service(id, token):
#     post = read_all_services()
#     if read_token(id) != token:
#         return "{'error':'token is deprecated'}"
#
#     to_json_keys = ['services_name', 'payment_amount', 'date_services', 'paid', 'name_lodgers', 'lodgers_id', 'address',
#                     'apartments_id']
#     post_json = {}
#     resilt_json = "["
#
#     for i in range(len(post)):
#         for index, value in enumerate(post[i]):
#             if index != 2:
#                 post_json[to_json_keys[index]] = value
#             else:
#                 post_json[to_json_keys[index]] = "'" + str(value) + "'"
#         resilt_json += json.dumps(post_json) + ", "
#         post_json.clear()
#
#     resilt_json = resilt_json[:len(resilt_json) - 2] + "]"
#     return resilt_json


@app.route('/pay_service/', methods=['POST'])
def pay_service():
    post = request.json
    if int(read_token(post["lodgers_id"])[0]) != int(post["token"]):
        return "{'error':'token is deprecated'}", 400

    ret = pay_services(post["lodgers_id"], post["date_services"], post["name_services"])

    post_json = {}

    return "{}", 200


# @app.route('/delete_service/', methods=['POST'])
# def service_delete():
#     post = request.json
#     if read_token(post["id"]) != post["token"]:
#         return "{'error':'token is deprecated'}"
#     ret = delete_service(post["services_id"])
#
#     return "all good"


if __name__ == "__main__":
    app.run()
