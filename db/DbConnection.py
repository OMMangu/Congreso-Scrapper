from abc import ABC, abstractmethod

from vote import Vote


class DbConnection(ABC):
    def __init__(self, host: str, database: str, user: str, pwd: str):
        self.host = host
        self.database = database
        self.user = user
        self.pwd = pwd
        self.conn = self.get_connection()

    @abstractmethod
    def get_connection(self):
        pass

    @abstractmethod
    def title_is_present(self, vote: Vote):
        pass

    @abstractmethod
    def insert(self, vote: Vote):
        pass

    @abstractmethod
    def get_similar_votes(self, group_a, group_b, group_c):
        pass
