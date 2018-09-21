from peewee import *
import datetime
from database.model.base_model import BaseModel


class ActionLogModel(BaseModel):

    _id = CharField(primary_key=True, max_length=300,null=False, column_name='id')
    user_id = CharField(max_length=300, null=False)
    action_name = CharField(max_length=300, null=False)
    action_type = CharField(max_length=300, null=False)
    action_msg = TextField()
    action_status = CharField(max_length=300, null=False)
    created_at = DateTimeField(default=datetime.datetime.now, null=False)

    class Meta:
        table_name = 'ActionLog'
