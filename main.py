import json
import random
import datetime
import psycopg2
from flask import Flask, request

app = Flask(__name__)


def create_apartments(you_address):
    conn = psycopg2.connect(dbname="Base_Of_Tenants", user="postgres", password="pass2tihon", host="localhost")
    with conn:
        with conn.cursor() as cursor:


            cursor.execute(f"Insert into apartments(address) values('{you_address}');")
    # records = cursor.fetchall()
            conn.commit()

            cursor.execute(f"Select address, apartments_id from apartments where address = '{you_address}'")
            records = cursor.fetchall()

    return records



def read_apartments(apartments_id):
    conn = psycopg2.connect(dbname="Base_Of_Tenants", user="postgres", password="pass2tihon", host="localhost")
    with conn:
        with conn.cursor() as cursor:



            cursor.execute(f"Select address from apartments where apartments_id = '{apartments_id}'")
            records = cursor.fetchall()

    return records


def read_all_apartments():
    conn = psycopg2.connect(dbname="Base_Of_Tenants", user="postgres", password="pass2tihon", host="localhost")
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(f"Select apartments_id, address from apartments")
            records = cursor.fetchall()

    return records


def update_apartments(you_address, new_lodgers):
    cursor = conn.cursor()


    cursor.execute(f"Select lodgers_id from lodgers where name_lodgers = '{new_lodgers}'")
    records = cursor.fetchall()
    cursor.execute(f"UPDATE apartments SET lodgers_id = {records[0][0]} WHERE address= '{you_address}';")
    conn.commit()
    cursor.execute(f"Select address, name_lodgers from apartments, lodgers where apartments.lodgers_id = '{new_lodgers}' and lodgers.lodgers_id = '{new_lodgers}'")
    records = cursor.fetchall()
    cursor.close()

    conn.close()
    return records


def delete_apartments(apartments_id):
    conn = psycopg2.connect(dbname="Base_Of_Tenants", user="postgres", password="pass2tihon", host="localhost")
    with conn:
        with conn.cursor() as cursor:

            cursor.execute(f"Delete from apartments Where apartments_id = '{apartments_id}'")
            conn.commit()

    return "deletion completed"

def create_lodgers(name_lodgers, login, password):
    conn = psycopg2.connect(dbname="Base_Of_Tenants", user="postgres", password="pass2tihon", host="localhost")
    with conn:
        with conn.cursor() as cursor:

            cursor.execute(f"Insert into lodgers(name_lodgers,login,password) values('{name_lodgers}','{login}','{password}');")
            # records = cursor.fetchall()
            conn.commit()
            cursor.execute(f"Select * from lodgers where name_lodgers = '{name_lodgers}'")
            records = cursor.fetchall()



    return records

def read_lodgers(lodgers_id):
    conn = psycopg2.connect(dbname="Base_Of_Tenants", user="postgres", password="pass2tihon", host="localhost")

    with conn:
        with conn.cursor() as cursor:




            cursor.execute(f"Select name_lodgers, lodgers_id, login, password, token from lodgers where lodgers.lodgers_id = '{lodgers_id}'")
            records = cursor.fetchall()
            conn.rollback()


    return records[0]

def read_all_lodgers():
    conn = psycopg2.connect(dbname="Base_Of_Tenants", user="postgres", password="pass2tihon", host="localhost")

    with conn:
        with conn.cursor() as cursor:




            cursor.execute("Select name_lodgers, lodgers_id, login, password, token from lodgers")
            records = cursor.fetchall()
            conn.rollback()


    return records

def delete_lodgers(id):
    conn = psycopg2.connect(dbname="Base_Of_Tenants", user="postgres", password="pass2tihon", host="localhost")

    with conn:
        with conn.cursor() as cursor:

            cursor.execute(f"Delete from lodgers Where lodgers_id = '{id}'")
            conn.commit()

    return "deletion completed"

def create_services(name_services, summ_of_payment, apartments_id, lodgers_id, date):
    conn = psycopg2.connect(dbname="Base_Of_Tenants", user="postgres", password="pass2tihon", host="localhost")

    with conn:
        with conn.cursor() as cursor:






            cursor.execute(f"Insert into services(services_name,payment_amount,apartments_id,lodgers_id, date_services) values('{name_services}',{summ_of_payment},{apartments_id},{lodgers_id},'{date}');")
            # records = cursor.fetchall()
            conn.commit()
            #cursor.execute(f"Select services_id, services_name,payment_amount,apartments_id,lodgers_id, date_services, paid from services where services_name = '{name_services}' AND lodgers_id = {lodgers_id} AND date_services = {date}")
            #records = cursor.fetchall()

    return "all good" #records
 
def read_services(lodgers_id):
    conn = psycopg2.connect(dbname="Base_Of_Tenants", user="postgres", password="pass2tihon", host="localhost")

    with conn:
        with conn.cursor() as cursor:



            cursor.execute(f"Select services_name, payment_amount, date_services, paid, name_lodgers, lodgers.lodgers_id, address, apartments.apartments_id from services, lodgers, apartments  where services.lodgers_id = {lodgers_id} AND services.apartments_id = apartments.apartments_id AND lodgers.lodgers_id = {lodgers_id}")
            records = cursor.fetchall()

    return records

def read_all_services():
    conn = psycopg2.connect(dbname="Base_Of_Tenants", user="postgres", password="pass2tihon", host="localhost")

    with conn:
        with conn.cursor() as cursor:



            cursor.execute(f"Select services_name, payment_amount, date_services, paid, name_lodgers, lodgers.lodgers_id, address, apartments.apartments_id from services, lodgers, apartments  where services.apartments_id = apartments.apartments_id AND services.lodgers_id = lodgers.lodgers_id")
            records = cursor.fetchall()

    return records


def pay_services(lodgers_id, date, name_services):
    conn = psycopg2.connect(dbname="Base_Of_Tenants", user="postgres", password="pass2tihon", host="localhost")

    with conn:
        with conn.cursor() as cursor:




            cursor.execute(f"UPDATE services SET paid = True WHERE lodgers_id = {lodgers_id} AND date_services = '{date}' AND services_name = '{name_services}';")
            # records = cursor.fetchall()
            conn.commit()
            cursor.execute(f"Select services_name, payment_amount, date_services, paid, name_lodgers, lodgers.lodgers_id, address, apartments.apartments_id from services, lodgers, apartments  where services.lodgers_id = {lodgers_id} AND services.apartments_id = apartments.apartments_id AND lodgers.lodgers_id = {lodgers_id} AND date_services = '{date}' AND services_name = '{name_services}'")
            records = cursor.fetchall()

    return records

def delete_service(service_id):
    conn = psycopg2.connect(dbname="Base_Of_Tenants", user="postgres", password="pass2tihon", host="localhost")

    with conn:
        with conn.cursor() as cursor:

            cursor.execute(f"Delete from services Where services_id = '{service_id}'")
            conn.commit()

    return "deletion completed"

def new_token(lodgers_id, token):
    conn = psycopg2.connect(dbname="Base_Of_Tenants", user="postgres", password="pass2tihon", host="localhost")

    with conn:
        with conn.cursor() as cursor:


#CURDATE()


            cursor.execute(f"UPDATE lodgers SET token = {token} WHERE lodgers_id = {lodgers_id};")
            # records = cursor.fetchall()
            conn.commit()


def read_token(lodgers_id):
    conn = psycopg2.connect(dbname="Base_Of_Tenants", user="postgres", password="pass2tihon", host="localhost")

    with conn:
        with conn.cursor() as cursor:




            cursor.execute(f"Select token, token_time from lodgers where lodgers_id = '{lodgers_id}'")
            records = cursor.fetchall()
            conn.commit()

    return records[0][0]

@app.route('/info/<int:id>/<int:token>')
def get_lodgers(id,token):

    post = read_lodgers(id)
    if read_token(id) != token:
        return "error please relogin"

    to_json_keys = ["name_lodgers", "lodgers_id", "login", "password", "token"]
    post_json = {}
    for index, value in enumerate(post):
        post_json[to_json_keys[index]] = value
    return json.dumps(post_json)


@app.route('/registration/', methods=['POST'])
def registration():
    post = request.json
    ret=create_lodgers(post["name"],post["login"],post["password"])

    return "all good"

@app.route('/login/', methods=['POST'])
def login():

    post = request.json
    ret=read_all_lodgers()
    for i in range(len(ret)):
        if ret[i][2] == post["login"] and ret[i][3] == post["password"]:
            new_token(ret[i][1], random.uniform(0,999999))
            print(read_token(ret[i][1]))
            return str(read_token(ret[i][1]))
    return "error"

@app.route('/delete_lodger/', methods=['POST'])
def delete_lodger():
    post = request.json
    if read_token(post["id"]) != post["token"]:
        return "error please relogin"
    ret = delete_lodger(post["id"])

    return "all good"

@app.route('/create_home/', methods=['POST'])
def create_home():

    post = request.json
    if read_token(post["id"]) != post["token"]:
        return "error please relogin"
    ret=create_apartments(post["address"])[0]

    to_json_keys = ['address', 'apartments_id']
    post_json = {}
    for index, value in enumerate(ret):
        post_json[to_json_keys[index]] = value
    return json.dumps(post_json)


@app.route('/get_home/<int:id>/<int:token>')
def get_home(id,token):

    post = read_all_apartments()
    if read_token(id) != token:
        return "error please relogin"

    to_json_keys = ['apartments_id', 'address']
    post_json = {}
    resilt_json = "["

    for i in range(len(post)):
        for index, value in enumerate(post[i]):
            post_json[to_json_keys[index]] = value
            print(i, index, value)
        resilt_json += json.dumps(post_json) + ", "
        post_json.clear()

    resilt_json = resilt_json[:len(resilt_json)-2]+"]"
    return resilt_json

@app.route('/delete_home/', methods=['POST'])
def delete_home():
    post = request.json
    if read_token(post["id"]) != post["token"]:
        return "error please relogin"
    ret = delete_apartments(post["apartments_id"])

    return "all good"

@app.route('/create_service/', methods=['POST'])
def create_service():

    post = request.json
    if read_token(post["id"]) != post["token"]:
        return "error please relogin"
    ret=create_services(post["name_services"], post["summ_of_payment"], post["apartments_id"], post["id"], post["date"])[0]

    to_json_keys = ['services_id', 'services_name', 'payment_amount', 'apartments_id', 'lodgers_id', 'date_services', 'paid']
    post_json = {}
    for index, value in enumerate(ret):
        post_json[to_json_keys[index]] = value
    return json.dumps(post_json)


@app.route('/get_service/<int:id>/<int:token>')
def get_service(id,token):

    post = read_services(id)
    if read_token(id) != token:
        return "error please relogin"

    to_json_keys = ['services_name', 'payment_amount', 'date_services', 'paid', 'name_lodgers', 'lodgers_id', 'address', 'apartments_id']
    post_json = {}
    resilt_json = "{"

    for i in range(len(post)):
        for index, value in enumerate(post[i]):
            if index != 2:
                post_json[to_json_keys[index]] = value
            else:
                post_json[to_json_keys[index]] = "'"+str(value)+"'"
        resilt_json += json.dumps(post_json) + ", "
        post_json.clear()

    resilt_json = resilt_json[:len(resilt_json)-2]+"}"
    print(resilt_json)
    return resilt_json


@app.route('/get_all_service/<int:id>/<int:token>')
def get_all_service(id,token):

    post = read_all_services()
    if read_token(id) != token:
        return "error please relogin"

    to_json_keys = ['services_name', 'payment_amount', 'date_services', 'paid', 'name_lodgers', 'lodgers_id', 'address', 'apartments_id']
    post_json = {}
    resilt_json = "{["

    for i in range(len(post)):
        for index, value in enumerate(post[i]):
            if index != 2:
                post_json[to_json_keys[index]] = value
            else:
                post_json[to_json_keys[index]] = "'"+str(value)+"'"
        resilt_json += json.dumps(post_json) + ", "
        post_json.clear()

    resilt_json = resilt_json[:len(resilt_json)-2]+"]}"
    print(resilt_json)
    return resilt_json


@app.route('/pay_service/', methods=['POST'])
def pay_service():

    post = request.json
    if read_token(post["id"]) != post["token"]:
        return "error please relogin"
    ret=pay_services(post["id"], post["date"], post["name_services"])
    print(ret)
    to_json_keys = ['services_name', 'payment_amount', 'date_services', 'paid', 'name_lodgers', 'lodgers_id', 'address', 'apartments_id']
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
    print(resilt_json)
    return resilt_json


@app.route('/delete_service/', methods=['POST'])
def service_delete():
    post = request.json
    if read_token(post["id"]) != post["token"]:
        return "error please relogin"
    ret = delete_service(post["services_id"])

    return "all good"


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run()

conn = psycopg2.connect(dbname="Base_Of_Tenants", user="postgres", password="pass2tihon", host="localhost")
print(read_all_lodgers())
conn.close()

