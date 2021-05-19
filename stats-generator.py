#!/usr/bin/python3
import json
import os
import unidecode
from mongoutils import insert


def read_json(name):
    with open(name, "r") as f:
        data = json.loads(f.read())
        return data


def get_json_list():
    path_list = [os.path.join(dirpath, filename) for dirpath, _, filenames in os.walk('./files') for filename in
                 filenames if filename.endswith('.json')]
    return path_list


def update_group(group, result_vote):
    unaccented_vote = unidecode.unidecode(result_vote)
    if unaccented_vote.upper() == "SI":
        group[0] = group[0] + 1
    elif unaccented_vote.upper() == "NO":
        group[1] = group[1] + 1
    elif unaccented_vote.upper() == "ABSTENCION":
        group[2] = group[2] + 1
    else:
        # No vota
        group[3] = group[3] + 1
    return group


def get_votos(json_data):
    grupos = {}
    group_list = set([x["grupo"] for x in json_data["votaciones"]])
    group_list = list(filter(lambda x: x != "", group_list))
    [grupos.setdefault(key, [0, 0, 0, 0]) for key in group_list]
    for voto in json_data["votaciones"]:
        group_name = voto["grupo"]
        if not group_name:
            continue
        result_vote = voto["voto"]
        group = grupos[group_name]
        update_group(group, result_vote)

    return grupos


def get_title(json_data):
    return json_data["informacion"]["textoExpediente"]


def get_date(json_data):
    return json_data["informacion"]["fecha"]


def main():
    name_list = get_json_list()
    for file in name_list:
        json_file = read_json(file)
        title = get_title(json_file)
        date = get_date(json_file)
        groups = get_votos(json_file)
        insert(title, date, groups)
        print("Inserted votes for {title}".format(title=title))


if __name__ == '__main__':
    main()
