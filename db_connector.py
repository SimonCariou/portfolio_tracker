from pymongo import MongoClient

class DatabaseConnector():
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.ticker_db
    
    def get_db(self):
        return self.db

    def get_client(self):
        return self.client
