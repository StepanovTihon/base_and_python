import json
import random

import psycopg2
from flask import Flask, request

app = Flask(__name__)


def create_apartments(you_address):
    cursor = conn.cursor()

    cursor.execute(f"Insert into apartments(address) values('{you_address}');")
    # records = cursor.fetchall()
    conn.commit()

    cursor.execute(f"Select * from apartments where address = '{you_address}'")
    records = cursor.fetchall()[0][0]
    cursor.close()

    conn.close()
    return records



def read_apartments(lodgers_id):
    cursor = conn.cursor()


    cursor.execute(f"Select address, name_lodgers from apartments, lodgers where apartments.lodgers_id = '{lodgers_id}' and lodgers.lodgers_id = '{lodgers_id}'")
    records = cursor.fetchall()
    cursor.close()

    conn.close()
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


def delete_apartments(you_address):
    cursor = conn.cursor()

    cursor.execute(f"Delete from apartments Where address = '{you_address}'")
    conn.commit()
    cursor.close()

    conn.close()
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

def delete_lodgers(name_lodgers):
    cursor = conn.cursor()

    cursor.execute(f"Delete from lodgers Where name_lodgers = '{name_lodgers}'")
    conn.commit()
    cursor.close()

    conn.close()
    return "deletion completed"

def create_services(name_services, summ_of_payment, address, name_lodgers, date):
    cursor = conn.cursor()



    cursor.execute(f"Select apartments_id from apartments where address = '{address}'")
    apartments_id = cursor.fetchall()[0][0]
    cursor.execute(f"Select lodgers_id from lodgers where name_lodgers = '{name_lodgers}'")
    lodgers_id = cursor.fetchall()[0][0]


    cursor.execute(f"Insert into services(services_name,payment_amount,apartments_id,lodgers_id, date_services) values('{name_services}',{summ_of_payment},{apartments_id},{lodgers_id},'{date}');")
    # records = cursor.fetchall()
    conn.commit()
    cursor.execute(f"Select * from services where services_name = '{name_services}' AND lodgers_id = '{lodgers_id} AND date_services = '{date}'")
    records = cursor.fetchall()
    cursor.close()

    conn.close()
    return records

def read_services(lodgers_id):
    cursor = conn.cursor()



    cursor.execute(f"Select services_name, payment_amount, date_services, paid, name_lodgers, address from services, lodgers, apartments  where services.lodgers_id = {lodgers_id} AND services.apartments_id = apartments.apartments_id")
    records = cursor.fetchall()
    cursor.close()

    conn.close()
    return records


def pay_services(lodgers_id, date, name_services):
    cursor = conn.cursor()




    cursor.execute(f"UPDATE services SET paid = True WHERE lodgers_id = {lodgers_id} AND date_services = '{date}' AND services_name = '{name_services}';")
    # records = cursor.fetchall()
    conn.commit()
    cursor.close()

    conn.close()
    return "service paid"

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
    if post[4] != token:
        return "error please relogin"

    to_json_keys = ['name_lodgers', 'lodgers_id', 'login', 'password']
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



@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run()

conn = psycopg2.connect(dbname="Base_Of_Tenants", user="postgres", password="pass2tihon", host="localhost")
print(read_all_lodgers())
conn.close()

