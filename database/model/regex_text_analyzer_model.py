# Created by Helic on 2018/8/1
from peewee import *
from database.model.base_model import BaseModel


class RegexTextAnalyzerModel(BaseModel):
    id = CharField(primary_key=True, max_length=128, null=False, column_name='id')
    keywords = TextField()
    target = CharField(max_length=200, null=False, default='all')
    logic = CharField(max_length=10, null=False, default='or')
    name = CharField(max_length=45, null=False)

    class Meta:
        table_name = 'regex_text_analyzer'

