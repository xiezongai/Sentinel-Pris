from peewee import *
import logging
import traceback
import uuid
import datetime
from database.model.statistic_model import StatisticModel

info_logger = logging.getLogger("info")
error_logger = logging.getLogger("error")
warning_logger = logging.getLogger("warning")


class StatisticDAO(object):

    @staticmethod
    def select_keywords_from_db(word, date_list):
        """
        关键词功能，给定一个词和一个时间范围，返回对应词的词频
        :param word: str,"word"
        :param date_list: ['2018-08-01 00:00:00', '2018-08-01 01:00:00']
        :return: {"word": "", "trending": [{
            "frequency": 25,
            "start_time": "2018-08-01 00:00:00",
            "end_time": "2018-08-01 01:00:00"
        }]}
        """
        try:
            results = (StatisticModel.select().where((StatisticModel.word == word) & (
                    StatisticModel.word_date << date_list))).execute()
            final_result = {"word": word, "trending": []}
            for row in results:
                final_result["trending"].append({
                    "frequency": row.word_frequency,
                    "start_time": row.word_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "end_time": (row.word_date + datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
                })
            return final_result
        except:
            error_logger.error("从数据库读取word frequency时发生其他错误, %s", traceback.format_exc(), extra={"host": 'localhost'})

    @staticmethod
    def select_hotwords_from_db(date_list, top=10):
        """
        给定一段时间，返回这段时间内前top词频的词
        :param date_list: ['2018-08-01 00:00:00', '2018-08-02 00:00:00']
        :param top: int
        :return: [{'word': '的', 'frequency': 56930}, {'word': '您', 'frequency': 37881}, {'word': '我', 'frequency': 28946}, {'word': '是', 'frequency': 26125}, {'word': '嗯', 'frequency': 18207}]
        """
        try:
            results = (StatisticModel.select(StatisticModel.word, fn.Sum(StatisticModel.word_frequency).alias('total'))
                       .where(StatisticModel.word_date << date_list).group_by(StatisticModel.word).order_by(
                fn.Sum(StatisticModel.word_frequency).desc()).limit(top)).execute()
            return [{"word": item.word, "frequency": int(item.total)} for item in results]
        except:
            error_logger.error("从数据库读取word frequency时发生其他错误, %s", traceback.format_exc(), extra={"host": 'localhost'})

    @staticmethod
    def timeSearchGerate(timestart, timeend):
        """
        :param timestart: date, "2018-01-01 00:00:00" str
        :param timeend:  date, "2018-01-02 01:00:00" str
        :return: ['2018-08-01 00:00:00',..., '2018-08-02 01:00:00']
        """
        resultlist = []
        datestart = datetime.datetime.strptime(timestart, '%Y-%m-%d %H:%M:%S').replace(minute=0, second=0)
        dateend = datetime.datetime.strptime(timeend, '%Y-%m-%d %H:%M:%S').replace(minute=0, second=0)
        while datestart <= dateend:
            resultlist.append(datestart.strftime('%Y-%m-%d %H:%M:%S'))
            datestart = datestart + datetime.timedelta(hours=1)
            # print (eachword,datestart.strftime('%Y-%m-%d'))
        return resultlist

    @staticmethod
    def insert_to_db(finalresult):
        """
        将结果写入到数据库中
        :param finalresult: {"2018-08-10"：[("你好",1)],"2018-08-11":[("联通",2)]}
        """
        try:
            for date in finalresult:
                for eachword in finalresult[date]:
                    wordmysql = eachword[0]
                    frequency = eachword[1]
                    StatisticModel.create(
                            id=str(uuid.uuid1()),
                            word=wordmysql,
                            word_date=str(date),
                            word_frequency=int(frequency)
                        )
        except Exception as e:
            error_logger.error("从数据库插入word时发生错误, %s", traceback.format_exc(), extra={"host": 'localhost'})

    @staticmethod
    def update_statistic(word, date, frequency):
        """
        更新statistic table
        @params word:str,待更新的词
        @params date:datetime,2018-09-13 00:00:01 ,str or datetime instance
        @params frequency:int

        @return None
        """
        try:
            if type(date) == str:
                date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            word_date = date.replace(minute=0, second=0)
            result = (StatisticModel.select().where((StatisticModel.word == word) & (StatisticModel.word_date == word_date))).execute()
            if len(result) == 0:
                StatisticModel.create(
                    id=str(uuid.uuid1()),
                    word=word,
                    word_date=str(word_date),
                    word_frequency=frequency
                )
            else:
                update_query = (StatisticModel.update({
                    StatisticModel.word_frequency: result[0].word_frequency + frequency
                }).where(StatisticModel.id == result[0].id)).execute()
        except Exception as e:
            error_logger.error("从数据库更新statistic时发生其他错误, %s, %s", str(e), traceback.format_exc(),
                               extra={"host": 'localhost'})


if __name__ == '__main__':
    keywords = StatisticDAO.select_keywords_from_db(word_list=["的", "你好"], date_list=['2018-08-01', '2018-08-02'])
    print(keywords)
    hotwords = StatisticDAO.select_hotwords_from_db(date_list=['2018-08-01', '2018-08-02'], top=5)
    print(hotwords)
