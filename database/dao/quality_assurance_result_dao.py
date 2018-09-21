import logging
import traceback
import uuid
import json
from database.model.quality_assurance_result import QualityAssuranceResult
from database.dao.regex_text_analyzer_dao import RegexTextAnalyzerDAO
from database.dao.smart_text_analyzer_dao import SmartTextAnalyzerDAO

info_logger = logging.getLogger("info")
error_logger = logging.getLogger("error")
warning_logger = logging.getLogger("warning")


class QualityAssuranceResultDAO(object):


    @staticmethod
    def get_total_results(dialog_id):
        results = (QualityAssuranceResult.select().where(QualityAssuranceResult.dialog_id==dialog_id)).execute()
        final_result = []
        for result in results:
            if result.analyzer_type == "smart_text_analyzer" :
                smart_text_analyzer=SmartTextAnalyzerDAO.view_analyzer_by_id(analyzer_id=result.analyzer_id)
                matched = []
                if result.result_m == 'True':
                    matched = json.loads(str(result.result_s), encoding='utf-8')
                final_result.append({
                    "result": True if result.result_m == 'True' else False,
                    'name': smart_text_analyzer["name"],
                    'type': "smart_text_analyzer",
                    'matched':matched
                })
            if result.analyzer_type == "regex_text_analyzer" :
                regex_text_analyzer=RegexTextAnalyzerDAO.view_analyzer_by_id(analyzer_id=result.analyzer_id)
                matched = []
                if result.result_m == 'True':
                    matched = json.loads(str(result.result_s), encoding='utf-8')
                final_result.append({
                    "result": True if result.result_m == 'True' else False,
                    'name': regex_text_analyzer["name"],
                    'type': "regex_text_analyzer",
                    'matched': matched
                })
            if result.analyzer_type == "smart_topic_analyzer":
                final_result.append({
                    "result":True,
                    'name': "topic_analyzer",
                    'type': "topic_analyzer",
                    'matched': json.loads(str(result.result_s), encoding='utf-8')
                })
        return final_result

    @staticmethod
    def create_smart_text_analyzer_result(dialog_id,analyzer_id,result_m,result_s):
        id = str(uuid.uuid1())
        result = QualityAssuranceResult.create(
            id = id,
            dialog_id=dialog_id,
            analyzer_id=analyzer_id,
            analyzer_type="smart_text_analyzer",
            result_m=result_m,
            result_s=result_s
        )
        if result.id==id:
            return True
        else:
            raise Exception("Cannot create smart text analyzer result with given parameters")

    @staticmethod
    def create_regex_text_analyzer_result(dialog_id,analyzer_id,result_m,result_s):
        try:
            id = str(uuid.uuid1())
            result = QualityAssuranceResult.create(
                id = id,
                dialog_id=dialog_id,
                analyzer_id=analyzer_id,
                analyzer_type="regex_text_analyzer",
                result_m=result_m,
                result_s=result_s
            )
            if result.id==id:
                return True
            else:
                raise Exception("Cannot create regex text analyzer result with given parameters")
        except Exception as e:
            error_logger.error("Error: , %s\nTraceback: %s", str(e), traceback.format_exc(), extra={"host": 'localhost'})


    @staticmethod
    def create_smart_topic_analyzer_result(dialog_id,result_m,result_s):
        try:
            id = str(uuid.uuid1())
            result = QualityAssuranceResult.create(
                id = id,
                dialog_id=dialog_id,
                analyzer_id="topic",
                analyzer_type="smart_topic_analyzer",
                result_m=result_m,
                result_s=result_s
            )
            if result.id==id:
                return True
            else:
                raise Exception("Cannot create smart topic analyzer result with given parameters")
        except Exception as e:
            error_logger.error("Error: , %s\nTraceback: %s", str(e), traceback.format_exc(), extra={"host": 'localhost'})
