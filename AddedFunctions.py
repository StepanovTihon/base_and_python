import json


def to_json(keys, values):
    post_json = {}
    print(values)
    for index, value in enumerate(values[0][0]):
        if keys[index] == "date":
            post_json[keys[index]] = value
        post_json[keys[index]] = value

    return post_json


def mass_to_json(keys, post):
    mass = []
    for p in range(len(post[0])):
        dictionary = dict.fromkeys(keys)
        for i in range(len(post[0][p])):
            if keys[i][0] == "d":
                print(str(post[0][p][i]))
                dictionary[keys[i]] = str(post[0][p][i])
            else:
                dictionary[keys[i]] = post[0][p][i]
        mass.append(dictionary)
    print(post)
    return json.dumps({'arr': mass})
