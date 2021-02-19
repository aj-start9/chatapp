from db import db


class ItemModel(db.Document):
    item = db.StringField(required=True)

    @classmethod
    def save_to_db(cls,item):
        item = cls(**item)
        item.save()

        
    @classmethod
    def get_from_db(cls):
        return cls.objects.all() 