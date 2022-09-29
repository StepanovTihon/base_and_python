import json
import random
import openpyxl
import time
from BaseWorkspace import *
from AddedFunctions import *
from datetime import date
from flask import Flask, request

# from dotenv import load_dotenv
errors = {
    400: "{'error':'Bad request'}",
    500: "{'error':'Internal server error'}",
    200: "{'error':'complited'}"
}

try:
    create_apartments("testaddress2")
except BaseError as be:
    print(be.txt)

# load_dotenv()
app = Flask(__name__)


@app.route('/info/<int:id>/<int:token>')
def get_lodgers(id, token):
    try:

        post = read_lodgers(id)

        if read_token(id) != token or post[0][5] < date.today():
            return '{"error":"token is deprecated"}', 400

        return json.dumps(
            to_json(["name_lodgers", "lodgers_id", "login", "password", "token", "token_time"], post)), 200

    except BadRequest:
        return '{"error":"BadRequest"}', 400
    except ServerError:
        return '{"error":"BaseError"}', 500


@app.route('/AllLodger/')
def get_all_lodgers():
    try:

        post = read_all_lodgers()

        post_json = {}
        to_json_keys = ['name_lodgers', 'lodgers_id', 'login', 'password', 'token']

        return mass_to_json(to_json_keys, post)

    except BadRequest:
        return '{"error":"BadRequest"}', 400
    except ServerError:
        return '{"error":"BaseError"}', 500


@app.route('/registration/', methods=['POST'])
def registration():
    try:

        post = request.json
        ret = create_lodgers(post["name"], post["login"], post["password"])

        return "{}", 200
    except BadRequest:
        return '{"error":"BadRequest"}', 400
    except ServerError:
        return '{"error":"BaseError"}', 500


@app.route('/login', methods=['POST'])
def login():
    try:
        post = request.json
        ret = read_all_lodgers()
        if len(ret) == 0:
            time.sleep(15)
            return errors[ret[1]], 400

        for i in range(len(ret)):

            if ret[i][2] == post["login"] and ret[i][3] == post["password"]:
                token = random.randint(0, 1000000)

                new_token(ret[i][1], token, (date.today() + datetime.timedelta(days=10)))

                return '{"token":"' + str(token) + '", "lodgers_id":' + str(ret[i][1]) + '}', 200

        time.sleep(15)
        return '{"error":"Bad request"}', 400
    except BadRequest:
        return '{"error":"BadRequest"}', 400
    except ServerError:
        return '{"error":"BaseError"}', 500


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
    try:
        post = request.json
        ret = create_apartments(post["address"])

        return "{}", 200
    except BadRequest:
        return '{"error":"BadRequest"}', 400
    except ServerError:
        return '{"error":"BaseError"}', 500


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
    try:
        post = request.json
        lodger = read_lodgers(post["lodgers_id"])
        if int(read_token(post["lodgers_id"])) != int(post["token"]) or lodger[0][5] < date.today():
            return "{'error':'token is deprecated'}", 400
        ret = create_services(post["services_name"], post["payment_amount"], post["apartments_id"], post["lodgers_id"],
                              post["date_services"])

        return "{}", 200
    except BadRequest:
        return '{"error":"BadRequest"}', 400
    except ServerError:
        return '{"error":"BaseError"}', 500


@app.route('/create_indication/', methods=['POST'])
def create_indication():
    try:
        post = request.json
        lodger = read_lodgers(post["lodgers_id"])
        if int(read_token(post["lodgers_id"])) != int(post["token"]) or lodger[0][5] < date.today():
            return "{'error':'token is deprecated'}", 400

        ret = create_indications(post["services_name"], post["apartments_id"], post["lodgers_id"],
                                 post["date_indications"],
                                 post["value_indications"])
        return "{}", 200
    except BadRequest:
        return '{"error":"BadRequest"}', 400
    except ServerError:
        return '{"error":"BaseError"}', 500


@app.route('/get_indication/<int:id>/<int:token>')
def get_indication(id, token):
    try:
        post = read_indications(id)
        lodger = read_lodgers(id)

        if int(read_token(id)) != int(token) or lodger[0][5] < date.today():
            return '{"error":"token is deprecated"}', 400

        to_json_keys = ["indications_id", "services_name", "apartments_id", "lodgers_id", "date_indications",
                        "value_indications"]

        return mass_to_json(to_json_keys, post)
    except BadRequest:
        return '{"error":"BadRequest"}', 400
    except ServerError:
        return '{"error":"BaseError"}', 500


@app.route('/get_service/<int:id>/<int:token>')
def get_service(id, token):
    try:
        post = read_services(id)
        lodger = read_lodgers(id)
        print(lodger[0][5], date.today(), lodger[0][5] < date.today())
        if read_token(id) != token or lodger[0][5] < date.today():
            return '{"error":"token is deprecated"}', 400

        to_json_keys = ['services_name', 'payment_amount', 'date_services', 'paid', 'name_lodgers', 'lodgers_id',
                        'address',
                        'apartments_id']
        post_json = {}

        return mass_to_json(to_json_keys, post)
    except BadRequest:
        return '{"error":"BadRequest"}', 400
    except ServerError:
        return '{"error":"BaseError"}', 500


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
    try:
        post = request.json
        lodger = read_lodgers(post["lodgers_id"])
        if int(read_token(post["lodgers_id"])) != int(post["token"]) or lodger[0][5] < date.today():
            return "{'error':'token is deprecated'}", 400

        ret = pay_services(post["lodgers_id"], post["date_services"], post["name_services"])

        post_json = {}

        return "{}", 200
    except BadRequest:
        return '{"error":"BadRequest"}', 400
    except ServerError:
        return '{"error":"BaseError"}', 500


@app.route('/get_excel/')
def get_excel():
    try:

        file = openpyxl.load_workbook('./Sample.xlsx')

        for apartment in read_all_apartments():
            sheet = file.copy_worksheet(file.active)
            sheet.title = apartment[1]
            sheet['A2'] = apartment[1]

            date = '0000-00-00'
            oy = 4
            services = []
            summ = 0
            for lodger in read_all_lodgers_and_address():
                if lodger[0][5] == apartment[0]:
                    services += read_services(lodger[1])

            services.sort(key=custom_key)

            for service in services:
                if to_number(service[2]) > to_number(date):
                    if date != '0000-00-00':
                        sheet['B' + str(oy)] = "итого:"
                        sheet['C' + str(oy)] = summ
                        summ = 0
                        oy += 2
                    date = service[2]
                    sheet['A' + str(oy)] = date
                sheet['B' + str(oy)] = service[0]
                sheet['C' + str(oy)] = service[1]
                sheet['D' + str(oy)] = read_lodgers(service[5])[0][0]
                summ += service[1]
                oy += 1
            sheet['B' + str(oy)] = "итого:"
            sheet['C' + str(oy)] = summ
            summ = 0

        file.save('abc.xlsx')

        return "{}", 200
    except BadRequest:
        return '{"error":"BadRequest"}', 400
    except ServerError:
        return '{"error":"BaseError"}', 500


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
