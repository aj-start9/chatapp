from db import db
from passlib.hash import sha256_crypt
from flask_login import LoginManager, UserMixin, login_user, login_required

class UserModel(db.Document,UserMixin):
    username = db.StringField(required=True)
    password = db.StringField()
    isVerified = db.BooleanField(required=True)
    name = db.StringField(required=True)
    image_url = db.StringField(required=True)
    authType = db.StringField(required=True)
    uid = db.StringField()
    isAdmin =  db.BooleanField(required=True)
    
    @classmethod
    def save_to_db(cls,args):
        print('')
        if args['authType'] == 'email':
            args['password'] = UserModel.hash_generate(args['password']) 
        user = cls(**args)
        user.save()    
    
    @classmethod
    def get_from_db(cls,user_password,password):
        try:
            if UserModel.hash_verify(user_password,password):
               return True
            return False       
        except:
            return {'message':'Internal Error'},500
        else:
            return {'message':'user rgistred'},201

    @staticmethod
    def hash_generate(password):
        return sha256_crypt.encrypt(password)

    @staticmethod
    def hash_verify(hash_test,password):
        return sha256_crypt.verify(hash_test,password)    

    @classmethod
    def find_by_username(cls,username):
        try:
            user = cls.objects.get(username=username)
        except:
            return None    
        else:
            return user

    def get_id(self):
        return self.username        

   
        
         



    
