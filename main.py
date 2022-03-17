import psycopg2


def search_for_matches(massiv):
    tmp_apartments = 0
    tmp_lodgers = 0
    tmp_services = 0
    for x in massiv:
        if x == "apartments":
            tmp_apartments = 1
    for x in massiv:
        if x == "lodgers":
            tmp_lodgers = 1
    for x in massiv:
        if x == "services":
            tmp_services = 1
    if tmp_apartments + tmp_services + tmp_lodgers == 3:
        return " Where apartments.apartments_id = services.apartments_id AND lodgers.lodgers_id = services.lodgers_id;"
    elif tmp_apartments + tmp_services == 2:
        return " Where apartments.apartments_id = services.apartments_id;"
    elif tmp_lodgers + tmp_services == 2:
        return " Where lodgers.lodgers_id = services.lodgers_id;"

    else:
        return ";"



def sample(columns, tabels):
    tmpselect = "SELECT "
    for x in columns:
        tmpselect += x + ", "
    tmpselect = tmpselect[0:len(tmpselect) - 1]
    tmpselect += " From "
    for x in tabels:

        tmpselect += x + ", "
    tmpselect = tmpselect[0:len(tmpselect) - 1]
    tmpselect += search_for_matches(tabels)
    return tmpselect


def add(columns, values, tabels):
    resultsql = ""
    for i in range(len(tabels)):
        tmpselect = "INSERT INTO " + tabels[i] + " ("
        desired_indexes = []
        for x in range(len(columns)-1):
            tmp_to_split = columns[x].split(".")
            if tmp_to_split[0] == tabels[i]:
                desired_indexes.append(x)
                tmpselect += str(tmp_to_split[1]) + ","

        tmpselect = tmpselect[0:len(tmpselect) - 1]
        tmpselect += ") VALUES ("
        for x in range(len(values)-1):
            if x in desired_indexes:
                if isinstance(values[x], str):
                    tmpselect += "'" + str(values[x]) + "',"
                else:
                    tmpselect += str(values[x]) + ","
        tmpselect = tmpselect[0:len(tmpselect) - 1]
        tmpselect += "); "
        resultsql += tmpselect
    print(resultsql)
    return resultsql

def create_apartments_admin(you_address):
    cursor = conn.cursor()

    cursor.execute(f"Insert into apartments(address) values('{you_address}');")
    # records = cursor.fetchall()
    conn.commit()
    cursor.close()

    conn.close()



def read_apartments(lodgers_id):
    cursor = conn.cursor()


    cursor.execute(f"Select address from apartments where lodgers_id = '{lodgers_id}'")
    records = cursor.fetchall()
    cursor.close()

    conn.close()
    return records


def update_apartments_admin(you_address, new_lodgers):
    cursor = conn.cursor()


    cursor.execute(f"Select lodgers_id from lodgers where name_lodgers = '{new_lodgers}'")
    records = cursor.fetchall()
    cursor.execute(f"UPDATE apartments SET lodgers_id = {records[0][0]} WHERE address= '{you_address}';")
    conn.commit()
    cursor.close()

    conn.close()



def delete_apartments_admin(you_address):
    cursor = conn.cursor()

    cursor.execute(f"Delete from apartments Where address = '{you_address}'")
    conn.commit()
    cursor.close()

    conn.close()

def create_lodgers_admin(name_lodgers):
    cursor = conn.cursor()

    cursor.execute(f"Insert into lodgers(name_lodgers) values('{name_lodgers}');")
    # records = cursor.fetchall()
    conn.commit()
    cursor.close()

    conn.close()


def delete_lodgers_admin(name_lodgers):
    cursor = conn.cursor()

    cursor.execute(f"Delete from lodgers Where name_lodgers = '{name_lodgers}'")
    conn.commit()
    cursor.close()

    conn.close()

def create_services_admin(name_services, summ_of_payment, address, name_lodgers, date):
    cursor = conn.cursor()



    cursor.execute(f"Select apartments_id from apartments where address = '{address}'")
    apartments_id = cursor.fetchall()[0][0]
    cursor.execute(f"Select lodgers_id from lodgers where name_lodgers = '{name_lodgers}'")
    lodgers_id = cursor.fetchall()[0][0]


    cursor.execute(f"Insert into services(services_name,payment_amount,apartments_id,lodgers_id, date_services) values('{name_services}',{summ_of_payment},{apartments_id},{lodgers_id},'{date}');")
    # records = cursor.fetchall()
    conn.commit()
    cursor.close()

    conn.close()

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

conn = psycopg2.connect(dbname="Base_Of_Tenants", user="postgres", password="pass2tihon", host="localhost")
print(update_apartments_admin("address1","Platon"))
conn.close()

