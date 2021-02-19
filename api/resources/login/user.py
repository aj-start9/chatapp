from flask import request
from flask_restful import Resource, reqparse, Api
from models.user import UserModel
from flask_jwt_extended import create_access_token
from google.oauth2 import id_token
import datetime
import google.auth.transport.requests
import requests

class UserLogin(Resource):
    
    def post(self):
        if request.args.get('authType') == 'google':
            pass
        elif  request.args.get('authType') == 'email':
            parser = reqparse.RequestParser()
            parser.add_argument('username',
                        type=str,
                        required=True,
                        help="THis field cannot be blank"
                        )
            parser.add_argument('password',
                        type=str,
                        required=True,
                        help="THis field cannot be blank"
                        )
            data = parser.parse_args()
            user =  UserModel.find_by_username(data['username'])  
            if user is None: 
                username = data['username']
                return {'message':f"user {username}  not found"},400
        
            if UserModel.get_from_db(user.password,data['password']):
                expires = datetime.timedelta(days=365)
                
                access_token = create_access_token(identity=f"{user.username}",expires_delta=expires)
                return {'access_token':access_token}, 200
            else:
                return {'message':'username or password Incorrect'},400 
       