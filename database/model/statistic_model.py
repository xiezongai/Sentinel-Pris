from peewee import *
from database.model.base_model import BaseModel


class StatisticModel(BaseModel):
    id = CharField(primary_key=True, max_length=128, null=False, column_name='id')
    word = CharField(max_length=255, null=False)
    word_date = DateTimeField(null=False)
    word_frequency = IntegerField(null=False)

    class Meta:
        table_name = 'statistic'
