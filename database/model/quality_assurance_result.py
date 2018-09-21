from peewee import *
from database.model.base_model import BaseModel


class QualityAssuranceResult(BaseModel):

    id = CharField(primary_key=True, max_length=128, null=False, column_name='id')
    dialog_id = CharField(max_length=128, null=False, column_name='dialog_id')
    analyzer_id = CharField(max_length=128, null=False, column_name='analyzer_id')
    analyzer_type = CharField(max_length=128, null=False, column_name='analyzer_type')
    result_m = CharField(max_length=500, null=False, column_name='result_m')
    result_s = TextField(null=False)
    correction = TextField(null=True, default='')

    class Meta:
        table_name = 'quality_assurance_result'
