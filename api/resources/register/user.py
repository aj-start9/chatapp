from flask import request, jsonify
from flask_restful import Resource, reqparse, Api
from models.user import UserModel
from flask_jwt_extended import create_access_token,set_access_cookies
from google.oauth2 import id_token
from google.auth import jwt
import datetime
import google.auth.transport.requests
import requests
from flask_login import login_user,UserMixin


class User(UserMixin):
    pass

class UserRegister(Resource):
    
    def post(self):
        if request.args.get('authType') == 'google':
            parser = reqparse.RequestParser()
            parser.add_argument('token',
                        type=str,
                        required=True,
                        help="Token not provided"
                        )
            data = parser.parse_args() 
            payload = jwt.decode(data['token'], certs=None,verify = False, audience = None)
            user =  UserModel.find_by_username(payload['email'])
            expires = datetime.timedelta(days=365)
            if user:         
                      
                login_user(user,remember=True,force=True)
                return "Bad"
    
            else:
                request_auth = google.auth.transport.requests.Request()
                id_info = id_token.verify_oauth2_token(data['token'], request_auth, '245937553496-jj986qcag03f80buncc0grjq5mos2vun.apps.googleusercontent.com')
                if id_info['email'] != payload['email'] :
                    return "Invalid credentials  "
                try:
                    content = {
                        'username': id_info['email'],
                        'name':  id_info['name'],
                        'isVerified': True,
                        'image_url': id_info['picture'],
                        'authType': "google",
                        'uid':id_info['sub'],
                        'isAdmin': False
                    }
                    UserModel.save_to_db(content)        
                except:
                    return {'message':'Internal Error'},500
                else:
                    resp = jsonify({'login': True})
                    access_token = create_access_token(identity=f"{payload['email']}",expires_delta=expires)   
                    set_access_cookies(resp, access_token)
                    print(resp)
                    return resp, 200    
                
        elif request.args.get('authType') == 'email':
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
            if user: 
                return {'message':'user is already registered'},400
            content = {
                'username': data['username'],
                'password' : data['password'],
                'name':  'AAA',
                'isVerified': True,
                'image_url': " ",
                'authType': "email",
                'isAdmin': False
            }     
            try:
                UserModel.save_to_db(content)
            except:
                return {'message':'Internal Error'},500
            else:
                return {'message':'User registred'}, 201 

        


    
      


       
                                 
        

