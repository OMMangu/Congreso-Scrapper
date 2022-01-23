from abc import ABC, abstractmethod


class DbConnection(ABC):
    def __init__(self, host: str, database: str, user: str, pwd: str):
        self.host = host
        self.database = database
        self.user = user
        self.pwd = pwd

    @abstractmethod
    def get_connection(self):
        pass

    @abstractmethod
    def get_db(self):
        pass

    @abstractmethod
    def title_is_present(self, title, subtitle, date):
        pass

    @abstractmethod
    def insert(self, title, subtitle, date, values):
        pass
