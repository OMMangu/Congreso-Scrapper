#!/usr/bin/python3
import pymongo

from db.DbConnection import DbConnection
# ignoring old implementation
from vote import Vote


class MongoDb(DbConnection):
    def get_connection(self):
        # TODO Use proper pwd handling
        return pymongo.MongoClient(
            "mongodb://{user}:{password}@{host}:27017/".format(user=self.user, password=self.pwd, host=self.host))

    def title_is_present(self, vote: Vote):
        pass

    def insert(self, vote: Vote):
        pass
