# Created by Helic on 2018/7/30
from peewee import *
from database.model.base_model import BaseModel

#TODO: add new field created_at
class TopicModel(BaseModel):
    id = CharField(primary_key=True, max_length=128, null=False, column_name='id')
    matched_sentences = TextField()
    prob = FloatField(null=False, default=0.7)
    target = CharField(max_length=200, null=False, default='all')
    matched_prob = FloatField(null=False, default=0.95)
    name = CharField(max_length=45)

    class Meta:
        table_name = 'topic'

