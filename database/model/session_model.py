
from peewee import *
from database.model.base_model import BaseModel
import datetime

class SessionModel(BaseModel):

    id = CharField(primary_key=True, max_length=300,null=False, column_name='id')
    user_id = CharField(max_length=300, null=False)
    created_at = DateTimeField(default=datetime.datetime.now, null=False)


    class Meta:
        table_name = 'SessionModel'
