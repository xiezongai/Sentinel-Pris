from peewee import *
from database.model.base_model import BaseModel


class KeypointAnalyzerModel(BaseModel):  
    id = CharField(primary_key=True, max_length=128, null=False, column_name='id')
    topic = CharField(max_length=200, null=False)
    name = CharField(max_length=200, null=False)
    description = TextField()
    matched_sentences = TextField()   # \n分隔
    regex = TextField()   # \n分隔
    target = CharField(max_length=200, null=False, default='all')  # all,坐席,客户
    mode = CharField(max_length=200, null=False, default='all')  # all,levenshtein,regex
    levenshtein_threshold = FloatField(default=0.8) 
    word2vec_threshold = FloatField(default=0.9) 
    created_datetime = DateTimeField(null=False)

    class Meta:
        table_name = 'keypoint_analyzer'


