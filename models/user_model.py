import sqlite3
from alchemy_db import db

class UserModel(db.Model):
    __tablename__ = 'USERS'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(60))
    password = db.Column(db.String(60))

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        select_query = 'SELECT * FROM USERS WHERE username = ?'
        result = cursor.execute(select_query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        conn.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        select_query = 'SELECT * FROM USERS WHERE id = ?'
        result = cursor.execute(select_query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        conn.close()
        return user
