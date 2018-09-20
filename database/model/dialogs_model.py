from peewee import *
import datetime
from database.model.base_model import BaseModel


class Dialogs(BaseModel):

    id = CharField(primary_key=True, max_length=128, column_name='id')
    call_id = CharField(max_length=25, column_name='call_id')
    caller_no = CharField(max_length=25, column_name='caller_no')
    callee_no = CharField(max_length=25, column_name='callee_no')
    begin_time = DateTimeField()  # dialog_start_time
    end_time= DateTimeField()
    transcripts = TextField(default="")
    emotion=CharField(max_length=30, column_name='emotion', default='')
    silence=FloatField(default=0)
    interruption=CharField(max_length=200, column_name='interruption', default='')
    status=IntegerField(default=0)
    session_id= CharField(max_length=128, column_name='session_id')
    is_manual_rated = BooleanField(default=False)
    manual_score= IntegerField(default=0)
    manual_rating=TextField(default="")
    machine_score = IntegerField(default=0)
    created_at = DateTimeField(default=datetime.datetime.now, null=False)
    class Meta:
        table_name = 'dialogs'
