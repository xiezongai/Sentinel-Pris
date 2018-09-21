# Created by Helic on 2018/8/2
import logging
import traceback
import uuid
from peewee import OperationalError

info_logger = logging.getLogger("info")
error_logger = logging.getLogger("error")
warning_logger = logging.getLogger("warning")


class RepeatCallAnalyzerDAO(object):

    @staticmethod
    def load_repeat_call_analyzer(analyzer_id=None):
        """
        从repeat_call_analyzer table中根据analyzer_id读取analyzer

        :param analyzer_id: list<string> => ["id1","id2",...]
        :return: 数据库返回的RepeatCallAnalyzer instances
        """
        try:
            # analyzer_ids = analyzer_id.split(',')  # 自动转成list
            if analyzer_id:
                if type(analyzer_id) == str:  # 只输入单个analyzer
                    analyzer_id = [analyzer_id]
                analyzers = (RepeatCallAnalyzer.select().where(RepeatCallAnalyzer.id << analyzer_id))
            else:
                analyzers = (RepeatCallAnalyzer.select())  # 如果没有analyzer_id，默认查询所有analyzers
            # info_logger.info("analyzer_id:{}".format(analyzer_id))
            return analyzers
        except OperationalError as operational_e:
            error_logger.error("从zhongxin.repeat_call_analyzer数据库读取analyzer时发生连接数据库错误, %s,%s", str(
                operational_e), traceback.format_exc(), extra={"host": 'localhost'})
            raise BaseException("连接数据库发生错误")
        except:
            error_logger.error("从zhongxin.repeat_call_analyzer数据库读取analyzer时发生其他错误, %s", traceback.format_exc(), extra={
                "host": 'localhost'})
            raise BaseException("从zhongxin.repeat_call_analyzer数据库读取analyzer时发生其他错误")

    @staticmethod
    def create_repeat_call_analyzer(matched_sentences, prob, analyzer_type, description, time_interval, logic):
        """
        用户新建analyzer,存入zhongxin.repeat_call_analyzer

        :param
        :return bool
        """
        try:
            RepeatCallAnalyzer.create(
                id=str(uuid.uuid4()),
                matched_sentences=matched_sentences,  # string
                prob=float(prob),
                analyzer_type=analyzer_type,
                description=description,
                time_interval=int(time_interval),
                logic=logic
            )
        except OperationalError as operational_e:
            error_logger.error("记录RepeatCallAnalyzer到zhongxin.repeat_call_analyzer数据库时发生连接数据库错误, %s,%s",
                               str(operational_e), traceback.format_exc(),
                               extra={"host": 'localhost'})
            raise BaseException("连接数据库发生错误")
        except:
            error_logger.error("记录RepeatCallAnalyzer到zhongxin.repeat_call_analyzer数据库时发生其他错误, %s", traceback.format_exc(),
                               extra={"host": 'localhost'})
            raise BaseException("连接数据库发生错误")

    @staticmethod
    def modify_repeat_call_analyzer(analyzer):
        """
        修改repeat_call_analyzer，存入数据库
        :param analyzer: ["11be6f1e-aa16-43d8-935b-e2be21fb8171",
                            "你摸着自己良心我有说错吗\n你是变态啊",
                            0.7,
                            "重复来电",
                            "重复来电",
                            6,
                            "and"]
        :return:
        """
        try:
            RepeatCallAnalyzer.update(matched_sentences=analyzer[1], prob=float(analyzer[2]), analyzer_type=analyzer[3],
                                      description=analyzer[4], time_interval=int(analyzer[5]), logic=analyzer[6]).\
                                      where(RepeatCallAnalyzer.id == analyzer[0]).execute()
        except OperationalError as operational_e:
            error_logger.error("修改RepeatCallAnalyzer到zhongxin.repeat_call_analyzer数据库时发生连接数据库错误, %s,%s",
                               str(operational_e), traceback.format_exc(),
                               extra={"host": 'localhost'})
            raise BaseException("修改RepeatCallAnalyzer到zhongxin.repeat_call_analyzer数据库时发生连接数据库错误")
        except:
            error_logger.error("修改RepeatCallAnalyzer到zhongxin.repeat_call_analyzer数据库时发生其他错误, %s", traceback.format_exc(),
                               extra={"host": 'localhost'})
            raise BaseException("修改RepeatCallAnalyzer到zhongxin.repeat_call_analyzer数据库时发生其他错误")

    @staticmethod
    def delete_repeat_call_analyzer(analyzer_id):
        """
        从repeat_call_analyzer table中根据analyzer_id删除analyzer

        :param analyzer_id: list<string> => ["id1","id2",...]
        :return: 数据库返回的RepeatCallAnalyzer instances
        """
        try:
            # analyzer_ids = analyzer_id.split(',')  # 自动转成list
            if type(analyzer_id) == str:        # 只输入单个analyzer
                analyzer_id = [analyzer_id]
            # info_logger.info("????:{}".format(analyzer_id))
            RepeatCallAnalyzer.delete().where(RepeatCallAnalyzer.id << analyzer_id).execute()
        except OperationalError as operational_e:
            error_logger.error("从zhongxin.repeat_call_analyzer数据库删除analyzer时发生连接数据库错误, %s,%s", str(
                operational_e), traceback.format_exc(), extra={"host": 'localhost'})
            raise BaseException("连接数据库发生错误")
        except:
            error_logger.error("从zhongxin.repeat_call_analyzer数据库删除analyzer时发生其他错误, %s", traceback.format_exc(), extra={
                "host": 'localhost'})
            raise BaseException("从zhongxin.repeat_call_analyzer数据库删除analyzer时发生其他错误")

