import json


def to_json(keys, values):
    post_json = {}

    for index, value in enumerate(values[0]):
        if keys[index][0] == "d" or keys[index] == "token_time":
            post_json[keys[index]] = str(value)
        else:
            post_json[keys[index]] = value


    return post_json


def mass_to_json(keys, post):
    mass = []
    for p in range(len(post)):
        dictionary = dict.fromkeys(keys)
        for i in range(len(post[p])):

            if keys[i][0] == "d" or keys[i] == "token_time":


                dictionary[keys[i]] = str(post[p][i])
            else:
                dictionary[keys[i]] = post[p][i]
        mass.append(dictionary)

    return json.dumps({'arr': mass})


def to_number(date):
    return str(date).split("-")[0] + str(date).split("-")[1] + str(date).split("-")[2]


def custom_key(def_service):
    return def_service[2]
