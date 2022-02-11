#!/usr/bin/python3

import unidecode


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
    return __get_json_attribute(json_data, "textoExpediente")


def get_subtitle(json_data):
    return __get_json_attribute(json_data, "textoSubGrupo")


def get_sesion(json_data):
    return __get_json_attribute(json_data, "sesion")


def get_num_votacion(json_data):
    return __get_json_attribute(json_data, "numeroVotacion")


def get_record_text(json_data):
    return __get_json_attribute(json_data, "textoExpediente")


def get_subgroup(json_data):
    return __get_json_attribute(json_data, "textoSubGrupo")


def get_detailed_vote(json_data):
    return json_data["votaciones"]


def __get_json_attribute(json_data, attribute):
    return json_data["informacion"][attribute]
