from peewee import *
from database.model.base_model import BaseModel


class QualityAssuranceResult(BaseModel):

    id = CharField(primary_key=True, max_length=128, null=False, column_name='id')
    dialog_id = CharField(max_length=128, null=False, column_name='dialog_id')  # 对应 dialogs table 的 id
    analyzer_id = CharField(max_length=128, null=False, column_name='analyzer_id') # 这个analyzer_id应该与smart_text_analyzer table中的id一致,或者topic id[设为topic],以及其它的analyzer id
    analyzer_name = CharField(max_length=128, null=False, column_name='analyzer_name') # 这个analyzer_name应该与smart_text_analyzer table中的name一致,或者topic name[设为topic],以及其它的analyzer name
    analyzer_type = CharField(max_length=128, null=False, column_name='analyzer_type') # 这个analyzer_type是用来区别text_analyzer,topic_analyzer，以及以后会添加的analyzer。主要是方便检索模块读表建立索引 => 取值为 "smart_text_analyzer" or "topic_analyzer" or "keypoint_analyzer"[话术分析器]
    result_m = CharField(max_length=1000, null=False, column_name='result_m')  # 粗略结果（见下列说明）
    result_s = TextField(null=False)  # 详细结果（见下列说明）
    correction = TextField(null=True, default='')  # TODO

    class Meta:
        table_name = 'quality_assurance_result'

'''
`result_m` 格式说明 : 
* 如果analyzer_type == "smart_text_analyzer": true or false [只要匹配到对话中的任何一处，即为true；否则为false]
* 如果analyzer_type == "topic_analyzer": topic [ML预测的第一个标签]
* 如果analyzer_type == "keypoint_analyzer": "关键点1,关键点2,..." [匹配到的所有关键点]
 
`result_s` 格式说明: 
* 如果analyzer_type == "smart_text_analyzer": 
```python
# 实际上是对应analyzer test function返回结果,dump之后存入该字段
{
        "dialog_id": str,
        "matched": [
                {
                    "score": 0.5454545454545454,  # 对于regex, score=1
                    "source": "没有了",            # 对话句子  
                    "matched": "",                # 保持格式一致，此处置空
                    "start_time": "08:06:38",
                    "end_time": "08:06:43",
                    "origin": "没有了没有了",       # 对话句子，与source保持一致
                    "regex": ""                   # regex pattern
                }],
        "transcripts": str(dumped),
        "target": str
}
```
* 如果analyzer_type == "topic_analyzer":
```python
# 实际上是对应analyzer test function返回结果,dump之后存入该字段
[
    {"topic": "XXX", "score": "XXX"}, {"topic": "XXX", "score": "XXX"}
]
```
* 如果analyzer_type == "keypoint_analyzer":
```python
# 实际上是对应analyzer test function返回结果,dump之后存入该字段
{
            "dialog_id": str,
            "matched": [
                            {'keypoint':'关键点1',
                            'matched':[{'sentence':'',         # 切割后的句子
                                        'compared_source':'',  # 匹配库中的句子
                                        'source_sentence':'',  # 对话中的原句（未切割）
                                        'score': float,
                                        "keywords": str,      # 匹配到的关键词
                                        "start_time": "08:06:38",
                                        "end_time": "08:06:43",
                                        },
                                        {},,,
                                ]
                            },
                            {'keypoint':'关键点2',
                            'matched':[{'sentence':'',  # 切割后的句子
                                        'compared_source':'',  # 匹配库中的句子
                                        'source_sentence':'',  # 对话中的原句（未切割）
                                        'score': float,
                                        "keywords": str,      # 匹配到的关键词
                                        "start_time": "08:06:38",
                                        "end_time": "08:06:43",
                                        },
                                        {},,,
                                ]
                            }
                        ],
            "transcripts": str(dumped)
}
```
'''