import sqlite3
from flask_restful import Resource, reqparse
from models.user_model import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type = str,
        required = True,
        help = 'Username cannot be blank'
    )
    parser.add_argument('password',
        type = str,
        required = True,
        help = 'Password cannot be blank'
    )
    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message':'Username already exists'},400

        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        query = 'INSERT INTO USERS VALUES(NULL, ?, ?)'
        conn.execute(query, (data['username'], data['password']))

        conn.commit()
        conn.close()

        return {'message':'User created successfully'},201
