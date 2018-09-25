# Created by Helic on 2018/7/30
from peewee import *
from database.model.base_model import BaseModel


class SmartTextAnalyzerModel(BaseModel):  
    id = CharField(primary_key=True, max_length=128, null=False, column_name='id')
    name = CharField(max_length=200, null=False)
    description = TextField()
    target = CharField(max_length=200, null=False, default='all')  # all,坐席,客户
    matched_sentences = TextField()   # \n分隔
    threshold = FloatField(null=False, default=0.8)
    regex = TextField()   # \n分隔
    mode = CharField(max_length=200, null=False, default='all')  # all,levenshtein,regex
    created_datetime = DateTimeField(null=False)

    class Meta:
        table_name = 'smart_text_analyzer'


if __name__ == '__main__':
    SmartTextAnalyzerModel.create_table()  
