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



conn = psycopg2.connect(dbname="Base_Of_Tenants", user="postgres", password="pass2tihon", host="localhost")
cursor = conn.cursor()


cursor.execute(add(["lodgers.name_lodgers", "lodgers.lodgers_id", "apartments.apartments_id", "apartments.address", "services.services_id", "services.services_name", "services.payment_amount", "services.apartments_id", "services.lodgers_id", "services.date_services"], ["Roma", 4, 4, "address4", 5, "Water", 5000, 4, 4, "2022-02-01"], ["apartments", "lodgers", "services"]))
#records = cursor.fetchall()
conn.commit()
cursor.close()

conn.close()
#print(records)
