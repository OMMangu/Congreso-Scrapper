#!/usr/bin/python3
import pymongo


def get_connection():
    #TODO Use proper pwd handling
    return pymongo.MongoClient("mongodb://{user}:{password}@localhost:27017/".format(user="test", password="test1"))


def get_db(connection):
    return connection["votes-db"]


def insert(title, date, values):
    db = get_db(get_connection())
    votes_collections = db["votes-col"]
    to_insert = {"title": title, "date": date, "values": values}
    x = votes_collections.insert_one(to_insert)
    return x

