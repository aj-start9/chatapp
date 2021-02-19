from flask import request,jsonify,json   
from flask_restful import Resource, reqparse, Api
from models.item import ItemModel
from flask_jwt_extended import jwt_required,get_jwt_identity
from socket_io import socketio
from flask_socketio import send, emit,Namespace
from bson.json_util import loads, dumps
import json
from flask_login import login_required,current_user,login_required

class Item(Resource,Namespace):
    # @jwt_required
    @login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('item',
                    type=str,
                    required=True,
                    help="Item not provided"
                    )
        data = parser.parse_args()
        try:
            ItemModel.save_to_db({'item':data['item']})
        except:
            return{'message':'Error'}
        else:
            return {'message':'saved item'}  
    
    @socketio.on('push')
    def test_connect(json):
        print(json)
        try:
            ItemModel.save_to_db(json)
            item = ItemModel.get_from_db()
            print(type(item.to_json()))    
        except:
            return     
        else:
            emit('news',{'items': item.to_json()},json=True, broadcast=True)

    @socketio.on('connect')
    # @jwt_required
    @login_required
    def test_get():
        print(current_user.is_authenticated) 
        if current_user.is_authenticated:
            print('yes')
        else:
            print('No')  
        item = None      
        try:
            item = ItemModel.get_from_db()
        except:
            return
        else:
            emit('news',{'items': item.to_json()},json=True, broadcast=True)    
       
    def get(self):  
        item = ItemModel.get_from_db()
        print(item.to_json())
        return (jsonify(item)) 