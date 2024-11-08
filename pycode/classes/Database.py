import sqlite3

class Database:
    def __init__(self):
        self.BANCO_PATH:str = './database.db'

    def __enter__(self):
        self.conn = sqlite3.connect(self.BANCO_PATH)
        return self.conn
    
    def __exit__(self, *args):
        self.conn.close()

# conn = sqlite3.connect('./banco.db')
# cursor = conn.cursor()