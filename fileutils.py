#!/usr/bin/python3
import json
import os
import re
import zipfile

import requests


def read_json(name):
    with open(name, "r") as f:
        data = json.loads(f.read())
        return data


def get_json_list():
    path_list = [os.path.join(dirpath, filename) for dirpath, _, filenames in os.walk('./files') for filename in
                 filenames if filename.endswith('.json')]
    path_list.sort()
    return path_list


def delete_zip(name):
    if os.path.isfile(name):
        os.remove(name)


def unzip_file(filename):
    with zipfile.ZipFile(filename, "r") as zip_ref:
        for info in zip_ref.infolist():
            if re.match(r'.+\.json', info.filename):
                zip_ref.extract(info, "files/")


def create_download_folder(folder):
    if os.path.isdir(folder):
        print("Skipping download folder creation")
    else:
        print("Creating download folder")
        os.mkdir(folder)


def get_zip(url, day, folder):
    r = requests.get(url)
    name = "{folder}/{DD}-{MM}-{YY}".format(folder=folder, DD=day.day, MM=day.month, YY=day.year)
    if os.path.isfile(name):
        print("Skipping {name}, already downloaded".format(name=name))
    else:
        print("Saving {name}".format(name=name))
        with open(name + ".zip", 'wb') as f:
            f.write(r.content)
    return name
