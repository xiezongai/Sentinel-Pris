# Created by Helic on 2018/8/1
import logging
import traceback
import uuid
from peewee import OperationalError
from database.model.regex_text_analyzer_model import RegexTextAnalyzerModel

info_logger = logging.getLogger("info")
error_logger = logging.getLogger("error")
warning_logger = logging.getLogger("warning")


class RegexTextAnalyzerDAO(object):

    @staticmethod
    def view_all_analyzers():
        try:
            analyzers = (RegexTextAnalyzerModel.select()).execute()
            packed_analyzers = []
            for analyzer in analyzers:
                packed_analyzers.append({
                    "id": analyzer.id,
                    "name": analyzer.name
                })
            return packed_analyzers
        except Exception as e:
            error_logger.error("从数据库读取Analyzer时发生其他错误, %s", traceback.format_exc(), extra={"host": 'localhost'})

    @staticmethod
    def view_analyzer_by_id(analyzer_id):
        try:
            analyzers = (RegexTextAnalyzerModel.select().where(RegexTextAnalyzerModel.id == analyzer_id)).execute()
            if len(list(analyzers)) == 1:
                return {
                    "id": analyzers[0].id,
                    "name": analyzers[0].name,
                    "keywords": analyzers[0].keywords.split('，'),
                    "target": analyzers[0].target,
                    "logic": analyzers[0].logic
                }
            else:
                return None
        except:
            error_logger.error("从数据库读取Analyzer时发生其他错误, %s", traceback.format_exc(), extra={"host": 'localhost'})

    @staticmethod
    def create_analyzer(name, keywords, target, logic):
        '''
        @Description: 创建一个新的Analyzer根据给出来得所有信息
        @Return: None|<SmartTextAnalyzer>
        '''
        try:
            id = str(uuid.uuid4())
            find_analyzers = (RegexTextAnalyzerModel.select().where(RegexTextAnalyzerModel.name == name)).execute()
            if len(find_analyzers) != 0:
                return None
            else:
                RegexTextAnalyzerModel.create(
                    id=id,
                    keywords='，'.join(keywords),  # string
                    target=target,
                    logic=logic,
                    name=name
                )
                new_analyzer = (RegexTextAnalyzerModel.select().where(RegexTextAnalyzerModel.id == id)).execute()
                if len(list(new_analyzer)) == 0:
                    # TODO: Error Handling: Cannot Create a New Analyzer
                    return None
                else:
                    return {
                        "id": new_analyzer[0].id,
                        "name": new_analyzer[0].name,
                        "keywords": new_analyzer[0].keywords.split('，'),
                        "target": new_analyzer[0].target,
                        "logic": new_analyzer[0].logic
                    }
        except Exception as e:
            error_logger.error("从数据库读取 Regex Analyzer 时发生其他错误, %s", traceback.format_exc(), extra={"host": 'localhost'})

    @staticmethod
    def update_analyzer(id, new_analyzer):
        '''
        @Description: 更新Analyzer，根据给定的id和new_analyzer给出的需要更新的field
        @Params: id <string> 需要更新的analyzer的id
        @Params: new_analyzer: {
            "id": <string>,
            "name": <string>,
            "keywords": <string[]>,
            "target": <string>,
            "logic": <string>
        }
        @Return: {
            "id": <string>,
            "name": <string>,
            "keywords": <string[]>,
            "target": <string>,
            "logic": <string>
        }
        '''
        try:
            (RegexTextAnalyzerModel.update({
                RegexTextAnalyzerModel.name: new_analyzer[
                    'name'] if 'name' in new_analyzer else RegexTextAnalyzerModel.name,
                RegexTextAnalyzerModel.keywords: '，'.join(new_analyzer[
                                                               'keywords']) if 'keywords' in new_analyzer else RegexTextAnalyzerModel.keywords,
                RegexTextAnalyzerModel.logic: new_analyzer[
                    'logic'] if 'logic' in new_analyzer else RegexTextAnalyzerModel.logic,
                RegexTextAnalyzerModel.target: new_analyzer[
                    'target'] if 'target' in new_analyzer else RegexTextAnalyzerModel.target
            }).where(RegexTextAnalyzerModel.id == id)).execute()
            updated_analyzer = (RegexTextAnalyzerModel.select().where(RegexTextAnalyzerModel.id == id)).execute()
            return {
                "id": updated_analyzer[0].id,
                "target": updated_analyzer[0].target,
                "name": updated_analyzer[0].name,
                "keywords": updated_analyzer[0].keywords.split('，'),
                "logic": updated_analyzer[0].logic
            }
        except Exception as e:
            error_logger.error("从数据库读取Regex时发生其他错误, %s, %s", str(e), traceback.format_exc(),
                               extra={"host": 'localhost'})

    @staticmethod
    def delete_analyzer(analyzer_id):
        '''
        @Description: 删除Analyzr根据给定的分析器id
        @Params: analyzer_id <string> 分析器的id
        @Return: <number> 表示被删除的行的数量
        '''
        try:
            delete_query = RegexTextAnalyzerModel.delete().where(RegexTextAnalyzerModel.id == analyzer_id)
            affected_rows = delete_query.execute()
            return affected_rows
        except Exception as e:
            error_logger.error("从数据库读取Analyzer时发生其他错误, %s", traceback.format_exc(), extra={"host": 'localhost'})
