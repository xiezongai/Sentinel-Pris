# Created by Helic on 2018/7/29
import pymysql


def connect_to_db(host="localhost", port=3306, user="helic", passwd="root1234", db="zhongxin", charset="utf8"):
    try:
        db = pymysql.connect(host=host, port=port, user=user,
                             passwd=passwd, db=db, charset="utf8")
        cursor = db.cursor()
        return db, cursor
    except Exception:
        raise Exception("failed to connect to datebase")


def convert_dialogs_format(dialogs):
    """将peewee取出的对话转化为以下格式： {"id": [("user", "start_time", "end_time", "你摸着自己良心我有说错吗？"), ("customer_service", "start_time", "end_time", "你是变态啊")]"""
    result = {}
    for dialog in dialogs:
        dialog_id = dialog.call_id
        result[dialog_id] = []

        for row in dialog.content.split('\n'):
            try:
                target, start_time, end_time, sentence = row.split('\t')
                result[dialog_id].append(
                    ("user" if target == '0' else "customer_service", start_time, end_time, sentence)
                )
            except Exception:
                pass
    return result
