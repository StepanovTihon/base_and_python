import psycopg2
import datetime

f = open('.env.txt', 'r')
data = f.read().split("|")
errors = {
    400: "{'error':'Bad request'}",
    500: "{'error':'Internal server error'}",
    200: "{'error':'complited'}"
}


def existence_apartments(id, you_address=''):
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                f"Select * from apartments where address = '{you_address}'" if you_address != ''
                else f"Select * from apartments Where apartments_id = '{id}'")

            return cursor.fetchall()


def existence_lodgers(id=-1, login=''):
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(f"Select * from lodgers where login = '{login}'" if login != ''
                           else f"Select * from lodgers Where lodgers_id = '{id}'")

            return cursor.fetchall()


def existence_services(name_services, date, lodgers_id, service_id=-1):
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(f"Select * from services where services_name = '{name_services}' AND "
                           f"date_services = '{date}' AND lodgers_id = {lodgers_id}" if service_id == -1
                           else f"Select * from services where services_id = '{service_id}'")

            return cursor.fetchall()


def existence_indications(services_name, lodgers_id, date_indications):
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(f"Select * from indications where services_name = '{services_name}' AND "
                           f"date_indications = '{date_indications}' AND lodgers_id = {lodgers_id}")

            return cursor.fetchall()


def create_apartments(you_address):
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])

    with conn:
        with conn.cursor() as cursor:
            if len(existence_apartments(-1, you_address)) != 0:
                return []

            cursor.execute(f"Insert into apartments(address) values('{you_address}');")
            conn.commit()
            cursor.execute(f"Select address, apartments_id from apartments where address = '{you_address}'")
            records = cursor.fetchall()

            return records
    return []


def read_apartments(apartments_id):
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(f"Select address from apartments where apartments_id = '{apartments_id}'")
            records = cursor.fetchall()

            return records
    return []


def read_all_apartments():
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(f"Select apartments_id, address from apartments")
            records = cursor.fetchall()

            return records
    return []


def delete_apartments(apartments_id):
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])
    with conn:
        with conn.cursor() as cursor:
            if len(existence_apartments(apartments_id)) == 0:
                return []

            cursor.execute(f"Delete from apartments Where apartments_id = '{apartments_id}'")
            conn.commit()

            return []
    return []


def create_lodgers(name_lodgers, login, password):
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])
    with conn:
        with conn.cursor() as cursor:
            if len(existence_lodgers(login)) != 0:
                return []
            cursor.execute(
                f"Insert into lodgers(name_lodgers,login,password, token) values('{name_lodgers}','{login}',"
                f"'{password}', {int(random.random() * 10000)});")
            # records = cursor.fetchall()
            conn.commit()
            cursor.execute(
                f"Select name_lodgers, lodgers_id, login, password, token from lodgers where name_lodgers = '{name_lodgers}'")
            records = cursor.fetchall()
            return records
    return []


def read_lodgers(lodgers_id):
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(f"Select name_lodgers, lodgers_id, login, password, token from "
                           f"lodgers where lodgers.lodgers_id = '{lodgers_id}'")
            records = cursor.fetchall()
            conn.rollback()
            return records
    return []


def read_all_lodgers():
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])

    with conn:
        with conn.cursor() as cursor:
            cursor.execute("Select name_lodgers, lodgers_id, login, password, token from lodgers")
            records = cursor.fetchall()

            conn.rollback()

            return records
    return []


def delete_lodgers(id):
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])

    with conn:
        with conn.cursor() as cursor:
            if len(existence_lodgers(-1, login)) == 0:
                return []
            cursor.execute(f"Delete from lodgers Where lodgers_id = '{id}'")
            conn.commit()

            return []
    return []


def create_services(name_services, summ_of_payment, apartments_id, lodgers_id, date):
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])

    with conn:
        with conn.cursor() as cursor:
            if len(existence_services(name_services, date, lodgers_id)) != 0:
                return []
            cursor.execute(
                f"Insert into services(services_name,payment_amount,apartments_id,lodgers_id, date_services, paid) "
                f"values('{name_services}',{summ_of_payment},{apartments_id},{lodgers_id},'{date}', false);")
            # records = cursor.fetchall()
            conn.commit()

            records = cursor.fetchall()

            return records
    return []


def read_services(lodgers_id):
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(f"Select services_name, payment_amount, date_services, paid, name_lodgers, "
                           f"lodgers.lodgers_id, address, apartments.apartments_id from services, lodgers, apartments "
                           f" where services.lodgers_id = {lodgers_id} AND services.apartments_id = "
                           f"apartments.apartments_id AND lodgers.lodgers_id = {lodgers_id}")
            records = cursor.fetchall()

            return records
    return []


def read_all_services():
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(f"Select services_name, payment_amount, date_services, paid, name_lodgers, "
                           f"lodgers.lodgers_id, address, apartments.apartments_id from services, lodgers, apartments  "
                           f"where services.apartments_id = apartments.apartments_id AND services.lodgers_id = "
                           f"lodgers.lodgers_id")
            records = cursor.fetchall()

            return records
    return []


def pay_services(lodgers_id, date, name_services):
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])

    with conn:
        with conn.cursor() as cursor:
            if len(existence_services(name_services, date, lodgers_id)) == 0:
                return []
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

            return records
    return []


def delete_service(service_id):
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])

    with conn:
        with conn.cursor() as cursor:
            if len(existence_services('', '', -1, service_id)) == 0:
                return []
            cursor.execute(f"Delete from services Where services_id = '{service_id}'")
            conn.commit()

            return []
    return []


def create_indications(services_name, apartments_id, lodgers_id, date_indications, value_indications):
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])

    with conn:
        with conn.cursor() as cursor:
            if len(existence_indications(services_name, lodgers_id, date_indications)) != 0:
                return []
            cursor.execute(
                f"Insert into indications (services_name,value_indications,apartments_id,lodgers_id, date_indications) "
                f"values('{services_name}',{value_indications},{apartments_id},{lodgers_id},'{date_indications}');")
            # records = cursor.fetchall()
            conn.commit()
            cursor.execute(f"Select indications_id, services_name, apartments_id, lodgers_id, date_indications, "
                           f"value_indications from indications where services_name ='{services_name}' AND "
                           f"lodgers_id = {lodgers_id} AND date_indications = '{date_indications}'")
            records = cursor.fetchall()

            return records
    return []


def read_indications(lodgers_id):
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(f"Select indications_id, services_name, apartments_id, lodgers_id, date_indications, "
                           f"value_indications from indications where lodgers_id = {lodgers_id}")

            records = cursor.fetchall()

            return records
    return []


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
            return records
    return []


def read_token(lodgers_id):
    conn = psycopg2.connect(dbname=data[0], user=data[1], password=data[2], host=data[3])
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(f"Select token, token_time from lodgers where lodgers_id = '{lodgers_id}'")
            records = cursor.fetchall()
            conn.commit()

            return records[0][0]
    return []
