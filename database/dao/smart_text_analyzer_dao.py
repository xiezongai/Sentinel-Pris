# Created by Helic on 2018/7/30
import logging
import traceback
import uuid
import datetime
from peewee import OperationalError
from database.model.smart_text_analyzer_model import SmartTextAnalyzerModel

info_logger = logging.getLogger("info")
error_logger = logging.getLogger("error")
warning_logger = logging.getLogger("warning")


class SmartTextAnalyzerDAO(object):
    
    @staticmethod
    def view_all_analyzers():
        try:
            analyzers = (SmartTextAnalyzerModel.select()).execute()
            packed_analyzers = []
            for analyzer in analyzers:
                packed_analyzers.append({
                    "id": analyzer.id,
                    "name": analyzer.name
                })
            return packed_analyzers
        except Exception as e:
            error_logger.error("从数据库读取SmartTextAnalyzer时发生其他错误, %s", traceback.format_exc(), extra={"host": 'localhost'})

    @staticmethod
    def view_analyzer_by_id(analyzer_id):
        try:
            analyzers = (SmartTextAnalyzerModel.select().where(SmartTextAnalyzerModel.id == analyzer_id)).execute()
            if len(list(analyzers)) == 1:
                return {
                    "id": analyzers[0].id,
                    "name": analyzers[0].name,
                    "description": analyzers[0].description,
                    "target": analyzers[0].target,
                    "matched_sentences": analyzers[0].matched_sentences.split('\n'),  # list
                    "threshold": analyzers[0].threshold,
                    "regex": analyzers[0].regex.split('\n'),  # list
                    "mode": analyzers[0].mode,
                    "created_datetime": analyzers[0].created_datetime
                }
            else:
                return None
        except:
            error_logger.error("从数据库读取SmartTextAnalyzer时发生其他错误, %s", traceback.format_exc(), extra={"host": 'localhost'})

    @staticmethod
    def create_analyzer(name,description,regex,matched_sentences,target="all",threshold=0.8,mode="all",created_datetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
        '''
        @Description: 创建一个新的Analyzer，根据给出来的所有信息
        @param name: str, "辱骂指责"
        @param description: str, 解释信息
        @param target: str, 只有三种取值 "all" "坐席" "客户"
        @param matched_sentences: [str,str], 用户输入的匹配句，注意是一个list
        @param threshold: float, 句子相似度算法的阈值
        @param regex: [str,str], 正则表达式的pattern
        @param mode: str, 目前有三种取值: all,levenshtein,regex
        @param created_datetime: str
        @Return: None|<SmartTextAnalyzer>
        '''
        try:
            id = str(uuid.uuid4())
            find_analyzers = (SmartTextAnalyzerModel.select().where(SmartTextAnalyzerModel.name == name)).execute()
            if len(find_analyzers) != 0:
                return None
            else:
                SmartTextAnalyzerModel.create(
                    id=id,
                    name=name,
                    description=description,
                    target=target,
                    matched_sentences='\n'.join(matched_sentences),  # string
                    threshold=float(threshold),
                    regex='\n'.join(regex),  # string
                    mode=mode,
                    created_datetime=created_datetime
                )
                new_analyzer = (SmartTextAnalyzerModel.select().where(SmartTextAnalyzerModel.id == id)).execute()
                if len(list(new_analyzer)) == 0:
                    # TODO: Error Handling: Cannot Create a New Analyzer
                    return None
                else:
                    return {
                        "id": new_analyzer[0].id,
                        "name": new_analyzer[0].name,
                        "description": new_analyzer[0].description,
                        "target": new_analyzer[0].target,
                        "matched_sentences": new_analyzer[0].matched_sentences.split('\n'),  # list
                        "threshold": new_analyzer[0].threshold,
                        "regex": new_analyzer[0].regex.split('\n'),  # list
                        "mode": new_analyzer[0].mode,
                        "created_datetime": new_analyzer[0].created_datetime
                    }
        except Exception as e:
            error_logger.error("从数据库读取 SmartTextAnalyzer 时发生其他错误, %s", traceback.format_exc(), extra={"host": 'localhost'})

    @staticmethod
    def update_analyzer(id, new_analyzer):
        '''
        @Description: 更新Analyzer，根据给定的id和new_analyzer给出的需要更新的field
        @Params: id <string> 需要更新的analyzer的id
        @Params: new_analyzer: {
            "name": str,
            "description": str,
            "target": str,
            "matched_sentences": [str,str],  # list
            "threshold": float,
            "regex": [str,str],  # list
            "mode": str
        }
        @Return: {
            "id": str,
            "name": str,
            "description": str,
            "target": str,
            "matched_sentences": [str],  # list
            "threshold": float,
            "regex": [str],  # list
            "mode": str,
            "created_datetime": str
        }
        '''
        try:
            update_query = (SmartTextAnalyzerModel.update({
                SmartTextAnalyzerModel.name: new_analyzer[
                    'name'] if 'name' in new_analyzer else SmartTextAnalyzerModel.name,
                SmartTextAnalyzerModel.description: new_analyzer[
                    'description'] if 'description' in new_analyzer else SmartTextAnalyzerModel.description,
                SmartTextAnalyzerModel.matched_sentences: '\n'.join(new_analyzer[
                                                                        'matched_sentences']) if 'matched_sentences' in new_analyzer else SmartTextAnalyzerModel.matched_sentences,
                SmartTextAnalyzerModel.threshold: new_analyzer[
                    'threshold'] if 'threshold' in new_analyzer else SmartTextAnalyzerModel.threshold,
                SmartTextAnalyzerModel.target: new_analyzer[
                    'target'] if 'target' in new_analyzer else SmartTextAnalyzerModel.target,
                SmartTextAnalyzerModel.mode: new_analyzer[
                    'mode'] if 'mode' in new_analyzer else SmartTextAnalyzerModel.mode,
                SmartTextAnalyzerModel.regex: '\n'.join(new_analyzer[
                    'regex']) if 'regex' in new_analyzer else SmartTextAnalyzerModel.regex,
                SmartTextAnalyzerModel.created_datetime: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }).where(SmartTextAnalyzerModel.id == id)).execute()
            updated_analyzer = (SmartTextAnalyzerModel.select().where(SmartTextAnalyzerModel.id == id)).execute()
            return {
                "id": updated_analyzer[0].id,
                "name": updated_analyzer[0].name,
                "description": updated_analyzer[0].description,
                "target": updated_analyzer[0].target,
                "matched_sentences": updated_analyzer[0].matched_sentences.split('\n'),  # list
                "threshold": updated_analyzer[0].threshold,
                "regex": updated_analyzer[0].regex.split('\n'),  # list
                "mode": updated_analyzer[0].mode,
                "created_datetime": updated_analyzer[0].created_datetime
            }
        except Exception as e:
            error_logger.error("从数据库读取SmartTextAnalyzer时发生其他错误, %s, %s", str(e), traceback.format_exc(),
                               extra={"host": 'localhost'})

    @staticmethod
    def delete_analyzer(analyzer_id):
        '''
        @Description: 删除Analyzr根据给定的分析器id
        @Params: analyzer_id <string> 分析器的id
        @Return: <number> 表示被删除的行的数量
        '''
        try:
            delete_query = SmartTextAnalyzerModel.delete().where(SmartTextAnalyzerModel.id == analyzer_id)
            affected_rows = delete_query.execute()
            return affected_rows
        except Exception as e:
            error_logger.error("从数据库读取SmartTextAnalyzer时发生其他错误, %s", traceback.format_exc(), extra={"host": 'localhost'})
