import psycopg2
import datetime

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
                f"Insert into lodgers(name_lodgers,login,password, token) values('{name_lodgers}','{login}','{password}', {int(random.random() * 10000)});")
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
                f"Insert into services(services_name,payment_amount,apartments_id,lodgers_id, date_services, paid) "
                f"values('{name_services}',{summ_of_payment},{apartments_id},{lodgers_id},'{date}', false);")
            # records = cursor.fetchall()
            conn.commit()

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
