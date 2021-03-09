import mongoengine
from config.default import DB_URI

class Database:

    def __init__(self):
        try:
            self.db = mongoengine.connect('walletSys', host=DB_URI)
            print('db connected')
        except Exception as e:
            print('something went wrong' + e)

    def db_client(self):
        return self.db
