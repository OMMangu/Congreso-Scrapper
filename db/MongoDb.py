#!/usr/bin/python3
import pymongo

from db.DbConnection import DbConnection


class MongoDb(DbConnection):
    def get_connection(self):
        # TODO Use proper pwd handling
        return pymongo.MongoClient("mongodb://{user}:{password}@{host}:27017/".format(user=self.user, password=self.pwd, host=self.host))

    def get_db(self):
        return self.get_connection()[self.database]

    def title_is_present(self, title, subtitle, date):
        db = self.get_db()
        votes_collections = db["votes-col"]
        result = votes_collections.find_one({"title": title, "subtitle": subtitle, "date": date})
        return False if result is None else True

    def insert(self, title, subtitle, date, values):
        db = self.get_db()
        votes_collections = db["votes-col"]
        to_insert = {"title": title, "subtitle": subtitle, "date": date, "values": values}
        x = votes_collections.insert_one(to_insert)
        return x
