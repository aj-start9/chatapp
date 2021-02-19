from flask import Flask, render_template, jsonify
from flask_restful import Api
from blacklist import BLACKLIST
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin
from socket_io import socketio
from flask_login import LoginManager
from models.user import UserModel
from flask_login_manager import login_manager


app = Flask(__name__)
api = Api(app)
login_manager.init_app(app)


CORS(
    app,
    origins="http://localhost:3000",
    allow_headers=[
        "Content-Type",
        "Authorization",
        "Access-Control-Allow-Credentials",
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Methods"
    ],
    supports_credentials=True,
)
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_BLACKLIST_ENABLED'] = True  # enable blacklist feature
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  # allow blacklisting for access and refresh tokens
app.secret_key = 'jose'  # could do app.config['JWT_SECRET_KEY'] if we prefer
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb+srv://ankit9678:ankitjain@cluster0-zyjna.mongodb.net/chat_app?retryWrites=true&w=majority',
    'connect': False,
}
app.config['MONGODB_CONNECT'] = True

jwt = JWTManager(app)


@login_manager.user_loader
def user_loader(username):
    print(username)
    return UserModel.objects.get(username=username)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in BLACKLIST
    

from resources.register.user import UserRegister
from resources.item import Item
from resources.login.user import UserLogin

api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(Item, '/item')
socketio.on_namespace(Item('/item'))

if __name__ == '__main__':
    from db import db 
    socketio.init_app(app,cors_allowed_origins= "http://localhost:3000",cors_allowed_credentials = True)
    db.init_app(app) 
    app.run(port=5000,debug=True)
    
   