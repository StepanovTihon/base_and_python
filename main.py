import json
import random
import datetime
import time

import psycopg2
from flask import Flask, request

# from dotenv import load_dotenv

# load_dotenv()
app = Flask(__name__)
f = open('.env.txt', 'r')
data = f.read().split("|")
errors = {
    400: "{'error':'Bad request'}",
    500: "{'error':'Internal server error'}",
    200: "{'error':'complited'}"
}


def create_apartments(you_address):
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(f"Select * from apartments where address = '{you_address}'")

            if len(cursor.fetchall()) != 0:
                return [[], 400]

            cursor.execute(f"Insert into apartments(address) values('{you_address}');")
            conn.commit()
            cursor.execute(f"Select address, apartments_id from apartments where address = '{you_address}'")
            records = cursor.fetchall()

            return [records, 200]
    return [[], 500]


def read_apartments(apartments_id):
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(f"Select address from apartments where apartments_id = '{apartments_id}'")
            records = cursor.fetchall()

            return [records, 200]
    return [[], 500]


def read_all_apartments():
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(f"Select apartments_id, address from apartments")
            records = cursor.fetchall()

            return [records, 200]
    return [[], 500]


# def update_apartments(you_address, new_lodgers):
#     cursor = conn.cursor()
#     cursor.execute(f"Select lodgers_id from lodgers where name_lodgers = '{new_lodgers}'")
#     records = cursor.fetchall()
#     cursor.execute(f"UPDATE apartments SET lodgers_id = {records[0][0]} WHERE address= '{you_address}';")
#     conn.commit()
#     cursor.execute(f"Select address, name_lodgers from apartments, lodgers where apartments.lodgers_id = "
#                    f"'{new_lodgers}' and lodgers.lodgers_id = '{new_lodgers}'")
#     records = cursor.fetchall()
#     cursor.close()
#
#     conn.close()
#     return records


def delete_apartments(apartments_id):
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(f"Select * from apartments where apartments_id = '{apartments_id}'")

            if len(cursor.fetchall()) == 0:
                return [[], 400]

            cursor.execute(f"Delete from apartments Where apartments_id = '{apartments_id}'")
            conn.commit()

            return [[], 200]
    return [[], 500]


def create_lodgers(name_lodgers, login, password):
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(f"Select * from lodgers where login = '{login}'")
            if len(cursor.fetchall()) != 0:
                return [[], 400]
            cursor.execute(
                f"Insert into lodgers(name_lodgers,login,password) values('{name_lodgers}','{login}','{password}');")
            # records = cursor.fetchall()
            conn.commit()
            cursor.execute(
                f"Select name_lodgers, lodgers_id, login, password, token from lodgers where name_lodgers = '{name_lodgers}'")
            records = cursor.fetchall()
            return [records, 200]
    return [[], 500]


def read_lodgers(lodgers_id):
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(f"Select name_lodgers, lodgers_id, login, password, token from "
                           f"lodgers where lodgers.lodgers_id = '{lodgers_id}'")
            records = cursor.fetchall()
            conn.rollback()
            return [records, 200]
    return [[], 500]


def read_all_lodgers():
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])

    with conn:
        with conn.cursor() as cursor:
            cursor.execute("Select name_lodgers, lodgers_id, login, password, token from lodgers")
            records = cursor.fetchall()

            conn.rollback()

            return [records, 200]
    return [[], 500]


def delete_lodgers(id):
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(f"Select * from lodgers where lodgers_id = '{id}'")

            if len(cursor.fetchall()) == 0:
                return [[], 400]
            cursor.execute(f"Delete from lodgers Where lodgers_id = '{id}'")
            conn.commit()

            return [[], 200]
    return [[], 500]


def create_services(name_services, summ_of_payment, apartments_id, lodgers_id, date):
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(f"Select * from services where services_name = '{name_services}' AND "
                           f"date_services = '{date}' AND lodgers_id = {lodgers_id}")
            if len(cursor.fetchall()) != 0:
                return [[], 400]
            cursor.execute(
                f"Insert into services(services_name,payment_amount,apartments_id,lodgers_id, date_services) "
                f"values('{name_services}',{summ_of_payment},{apartments_id},{lodgers_id},'{date}');")
            # records = cursor.fetchall()
            conn.commit()
            cursor.execute(f"Select services_id, services_name,payment_amount, apartments_id,lodgers_id, "
                           f"date_services, paid from services where services_name ='{name_services}' AND "
                           f"lodgers_id = {lodgers_id} AND date_services = {date}")
            records = cursor.fetchall()

            return [records, 200]
    return [[], 500]


def read_services(lodgers_id):
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(f"Select services_name, payment_amount, date_services, paid, name_lodgers, "
                           f"lodgers.lodgers_id, address, apartments.apartments_id from services, lodgers, apartments "
                           f" where services.lodgers_id = {lodgers_id} AND services.apartments_id = "
                           f"apartments.apartments_id AND lodgers.lodgers_id = {lodgers_id}")
            records = cursor.fetchall()

            return [records, 200]
    return [[], 500]


def read_all_services():
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(f"Select services_name, payment_amount, date_services, paid, name_lodgers, "
                           f"lodgers.lodgers_id, address, apartments.apartments_id from services, lodgers, apartments  "
                           f"where services.apartments_id = apartments.apartments_id AND services.lodgers_id = "
                           f"lodgers.lodgers_id")
            records = cursor.fetchall()

            return [records, 200]
    return [[], 500]


def pay_services(lodgers_id, date, name_services):
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(f"Select * from services where services_name = '{name_services}' AND "
                           f"date_services = '{date}' AND lodgers_id = {lodgers_id}")
            if len(cursor.fetchall()) == 0:
                return [[], 400]
            cursor.execute(f"UPDATE services SET paid = True WHERE lodgers_id = {lodgers_id} AND date_services = "
                           f"'{date}' AND services_name = '{name_services}';")
            # records = cursor.fetchall()
            conn.commit()
            cursor.execute(f"Select services_name, payment_amount, date_services, paid, name_lodgers, "
                           f"lodgers.lodgers_id, address, apartments.apartments_id from services, lodgers, "
                           f"apartments  where services.lodgers_id = {lodgers_id} AND services.apartments_id = "
                           f"apartments.apartments_id AND lodgers.lodgers_id = {lodgers_id} AND date_services = "
                           f"'{date}' AND services_name = '{name_services}'")
            records = cursor.fetchall()

            return [records, 200]
    return [[], 500]


def delete_service(service_id):
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(f"Select * from services where services_id = '{service_id}'")

            if len(cursor.fetchall()) == 0:
                return [[], 400]
            cursor.execute(f"Delete from services Where services_id = '{service_id}'")
            conn.commit()

            return [[], 200]
    return [[], 500]


def create_indications(services_name, apartments_id, lodgers_id, date_indications, value_indications):
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(f"Select * from indications where services_name = '{services_name}' AND "
                           f"date_indications = '{date_indications}' AND lodgers_id = {lodgers_id}")
            if len(cursor.fetchall()) != 0:
                return [[], 400]
            cursor.execute(
                f"Insert into indications (services_name,value_indications,apartments_id,lodgers_id, date_indications) "
                f"values('{services_name}',{value_indications},{apartments_id},{lodgers_id},'{date_indications}');")
            # records = cursor.fetchall()
            conn.commit()
            cursor.execute(f"Select indications_id, services_name, apartments_id, lodgers_id, date_indications, "
                           f"value_indications from indications where services_name ='{services_name}' AND "
                           f"lodgers_id = {lodgers_id} AND date_indications = '{date_indications}'")
            records = cursor.fetchall()

            return [records, 200]
    return [[], 500]


def read_indications(lodgers_id):
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(f"Select indications_id, services_name, apartments_id, lodgers_id, date_indications, "
                           f"value_indications from indications where lodgers_id = {lodgers_id}")

            records = cursor.fetchall()

            return [records, 200]
    return [[], 500]


def new_token(lodgers_id, token):
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])

    with conn:
        with conn.cursor() as cursor:
            # CURDATE()
            cursor.execute(f"UPDATE lodgers SET token = {token} WHERE lodgers_id = {lodgers_id};")
            # records = cursor.fetchall()
            conn.commit()
            cursor.execute(f"Select token, token_time from lodgers where lodgers_id = '{lodgers_id}'")
            records = cursor.fetchall()
            return [records, 200]
    return [[], 500]


def read_token(lodgers_id):
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(f"Select token, token_time from lodgers where lodgers_id = '{lodgers_id}'")
            records = cursor.fetchall()
            conn.commit()

            return [records[0][0], 200]
    return [[], 500]


def to_json(keys, values):
    post_json = {}
    print(values)
    for index, value in enumerate(values[0][0]):
        if keys[index] == "date":
            post_json[keys[index]] = value
        post_json[keys[index]] = value

    return post_json


@app.route('/info/<int:id>/<int:token>')
def get_lodgers(id, token):
    post = read_lodgers(id)
    print(read_token(id)[0], token)
    if read_token(id)[0] != token:
        return '{"error":"token is deprecated"}', 401
    if len(post[0]) == 0:
        return errors[post[1]], 400
    return json.dumps(to_json(["name_lodgers", "lodgers_id", "login", "password", "token"], post)), 200


@app.route('/registration/', methods=['POST'])
def registration():
    post = request.json
    ret = create_lodgers(post["name"], post["login"], post["password"])
    if len(ret[0]) == 0:
        return errors[ret[1]]

    return json.dumps(to_json(['name_lodgers', 'lodgers_id', 'login', 'password', 'token'], ret))


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


@app.route('/delete_lodger/', methods=['POST'])
def delete_lodger():
    post = request.json
    if read_token(post["id"]) != post["token"]:
        return "{'error':'token is deprecated'}"
    ret = delete_lodger(post["id"])

    return "{'error':'Deleted'}"


@app.route('/create_home/', methods=['POST'])
def create_home():
    post = request.json
    if read_token(post["id"]) != post["token"]:
        return "{'error':'token is deprecated'}"
    ret = create_apartments(post["address"])

    if len(ret[0]) == 0:
        return errors[ret[1]]
    return json.dumps(to_json(['address', 'apartments_id'], ret))


@app.route('/get_home/<int:id>/<int:token>')
def get_home(id, token):
    post = read_all_apartments()
    if read_token(id) != token:
        return "{'error':'token is deprecated'}"

    to_json_keys = ['apartments_id', 'address']
    post_json = {}
    resilt_json = "["

    for i in range(len(post)):
        for index, value in enumerate(post[i]):
            post_json[to_json_keys[index]] = value

        resilt_json += json.dumps(post_json) + ", "
        post_json.clear()

    resilt_json = resilt_json[:len(resilt_json) - 2] + "]"
    return resilt_json


@app.route('/delete_home/', methods=['POST'])
def delete_home():
    post = request.json
    if read_token(post["id"]) != post["token"]:
        return "{'error':'token is deprecated'}"
    ret = delete_apartments(post["apartments_id"])

    return "{'error':'Deleted'}"


@app.route('/create_service/', methods=['POST'])
def create_service():
    post = request.json
    if read_token(post["id"]) != post["token"]:
        return "{'error':'token is deprecated'}"
    ret = create_service(post["services_name", "payment_amount", "apartments_id", "lodgers_id", "date_services"])
    return json.dumps(to_json(['services_id', 'services_name', 'payment_amount', 'apartments_id', 'lodgers_id',
                               'date_services', 'paid'], ret))


@app.route('/create_indication/', methods=['POST'])
def create_indication():
    post = request.json

    if int(read_token(post["lodgers_id"])[0]) != int(post["token"]):
        return "{'error':'token is deprecated'}", 400
    print(post["services_name"])
    ret = create_indications(post["services_name"], post["apartments_id"], post["lodgers_id"], post["date_indications"],
                             post["value_indications"])
    return "{}", 200


@app.route('/get_indication/<int:id>/<int:token>')
def get_indication(id, token):
    post = read_indications(id)
    print(read_token(id)[0], token)
    if int(read_token(id)[0]) != int(token):
        return '{"error":"token is deprecated"}'

    to_json_keys = ["indications_id", "services_name", "apartments_id", "lodgers_id", "date_indications","value_indications"]
    post_json = {}
    result_json = '{"arr":['

    for i in range(len(post[0])):
        for index, value in enumerate(post[0][i]):
            if index != 4:

                post_json[to_json_keys[index]] = value
            else:
                post_json[to_json_keys[index]] = str(value)
        result_json += json.dumps(post_json, ensure_ascii=False) + ", "
        post_json.clear()

    result_json = result_json[:len(result_json) - 2] + "]}"

    return result_json


@app.route('/get_service/<int:id>/<int:token>')
def get_service(id, token):
    post = read_services(id)
    print(read_token(id)[0], token)
    if read_token(id)[0] != token:
        return '{"error":"token is deprecated"}'

    to_json_keys = ['services_name', 'payment_amount', 'date_services', 'paid', 'name_lodgers', 'lodgers_id', 'address',
                    'apartments_id']
    post_json = {}
    result_json = '{"arr":['

    for i in range(len(post[0])):
        for index, value in enumerate(post[0][i]):
            if index != 2:

                post_json[to_json_keys[index]] = value
            else:
                post_json[to_json_keys[index]] = str(value)
        result_json += json.dumps(post_json, ensure_ascii=False) + ", "
        post_json.clear()

    result_json = result_json[:len(result_json) - 2] + "]}"

    return result_json


@app.route('/get_all_service/<int:id>/<int:token>')
def get_all_service(id, token):
    post = read_all_services()
    if read_token(id) != token:
        return "{'error':'token is deprecated'}"

    to_json_keys = ['services_name', 'payment_amount', 'date_services', 'paid', 'name_lodgers', 'lodgers_id', 'address',
                    'apartments_id']
    post_json = {}
    resilt_json = "["

    for i in range(len(post)):
        for index, value in enumerate(post[i]):
            if index != 2:
                post_json[to_json_keys[index]] = value
            else:
                post_json[to_json_keys[index]] = "'" + str(value) + "'"
        resilt_json += json.dumps(post_json) + ", "
        post_json.clear()

    resilt_json = resilt_json[:len(resilt_json) - 2] + "]"
    return resilt_json


@app.route('/pay_service/', methods=['POST'])
def pay_service():
    post = request.json
    if read_token(post["id"]) != post["token"]:
        return "{'error':'token is deprecated'}"
    ret = pay_services(post["id"], post["date"], post["name_services"])

    to_json_keys = ['services_name', 'payment_amount', 'date_services', 'paid', 'name_lodgers', 'lodgers_id', 'address',
                    'apartments_id']
    post_json = {}
    resilt_json = "{["

    for i in range(len(ret)):
        for index, value in enumerate(ret[i]):
            if index != 2:
                post_json[to_json_keys[index]] = value
            else:
                post_json[to_json_keys[index]] = "'" + str(value) + "'"
        resilt_json += json.dumps(post_json) + ", "
        post_json.clear()

    resilt_json = resilt_json[:len(resilt_json) - 2] + "]}"

    return resilt_json


@app.route('/delete_service/', methods=['POST'])
def service_delete():
    post = request.json
    if read_token(post["id"]) != post["token"]:
        return "{'error':'token is deprecated'}"
    ret = delete_service(post["services_id"])

    return "all good"


@app.route("/hello")
def hello():
    return "{'error':'hello world'}"


if __name__ == "__main__":
    app.run()
