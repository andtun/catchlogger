import sqlite3
import datetime

class DataBase:
    name = 'UserList.db'

    _db_connection = None
    _db_cur = None

    def __init__(self):
        self._db_connection = sqlite3.connect(self.name)
        self._db_cur = self._db_connection.cursor()

    def query(self, query):
        self._db_cur.execute(query)
        self._db_connection.commit()
        return

    def fetch(self, query):
        return self._db_cur.execute(query).fetchall()

    def save(self):
        self._db_connection.commit()

    def __del__(self):
        self._db_connection.close()

db = DataBase()
"""
db.query("CREATE TABLE Auth (uname TEXT, pw TEXT, email text, last_active INTEGER);")
"""

def createTable(uname):
    db.query("CREATE TABLE %s (link_num INTEGER PRIMARY KEY, link_itself TEXT, redir_addr TEXT);") % uname

def createLinkTable(uname, link):
    tablename = uname + "_" + link
    db.query("CREATE TABLE %S (addr_num INTEGER PRIMARY KEY);") % tablename

def create_user(username, pw, email):
    cmnd = "INSERT INTO Auth VALUES ('%s', '%s', '%s', 0);" % (username, pw, email)
    db.query(cmnd)

def set_timestamp(username):
    now = str(int(datetime.datetime.timestamp(datetime.datetime.now())))
    cmnd = "UPDATE Auth SET last_active=%s WHERE uname=%s;" % (now, username)


