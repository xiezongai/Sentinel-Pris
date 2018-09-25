"""
生成一些模拟数据，测试检索功能
"""
import datetime
import uuid
import pymysql
import random
import json


def connect_to_db(host="10.112.57.93", port=3306, user="root", passwd="2014pris", db="ellison", charset="utf8"):
    try:
        db = pymysql.connect(host=host, port=port, user=user,
                             passwd=passwd, db=db, charset="utf8")
        cursor = db.cursor()
        return db, cursor
    except Exception:
        raise Exception("failed to connect to datebase")


def select_all_data(cursor):
    try:
        sql = "select * from dialogs"
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
    except Exception:
        raise Exception("failed to select old data from dialog")


def generate():
    '''
    descreption:生成模拟数据，建立索引
    return id_num: ??? TODO 如果未赋值，插入None会有什么后果？
    return dialog_id : str
    return call_id : str
    return session_id : str
    return transcripts : str
    return begin_time : "2018-01-01 00:00:00" str
    return end_time : "2018-01-01 00:00:00" str
    return silence_max : float
    return silence_total : float
    return emotion : str, '积极'|'消极'|'中性'
    return interruption : bool
    return topic : str 业务标签
    return smart_text_analyzer : {"analyzer_name1": "True", "analyzer_name2": "False"} 所有文本分析器结果:True代表属于该分析器
    return keypoint_analyzer : ["关键点1","关键点2",...] 匹配到的所有关键点
    '''
    db, cursor = connect_to_db()
    results = select_all_data(cursor)
    for result in results:
        dialog_id = result[0]
        call_id = result[1]
        session_id = result[13]
        transcripts = result[6]
        begin_time = str(result[4])
        end_time = str(result[5])
        silence_max = result[8]
        silence_total = result[9]
        emotion = result[7]
        interruption = result[11]  # bool
        topic = random.choice(['微产品', '额度调整', '调额婉拒', '卡片挂失', '交易模式', '解除标志', '卡转卡办理', '卡片激活', '年费产品',
                               '设置密码', '现金分期', '延期还款', '溢缴款办理', '圆梦金大额消费分期', '账单单笔分期', '中收产品', '自动转账及购汇',
                               '查询修改账单日', '分期提前缴款'])
        smart_text_analyzer = {"答非所问": random.choice(["True", "False"]), "换位思考": random.choice(["True", "False"]), 
                                "辱骂指责": random.choice(["True", "False"]), "推诿": random.choice(["True", "False"]),
                                "用心超越期望": random.choice(["True", "False"]), "沟通技巧": random.choice(["True", "False"]), 
                                "把握需求": random.choice(["True", "False"])}
        keypoint_analyzer = list(set(random.choices(["关键点1","关键点2", "关键点3","关键点4", "关键点5","关键点6"], k=random.randint(0, 6))))
        yield {
            "dialog_id": dialog_id,
            "call_id": call_id,
            "session_id": session_id,
            "transcripts": transcripts,
            "begin_time": begin_time,
            "end_time": end_time,
            "silence_max": silence_max,
            "silence_total": silence_total,
            "emotion": emotion,
            "interruption": interruption,
            "topic": topic,
            "smart_text_analyzer": smart_text_analyzer,
            "keypoint_analyzer": keypoint_analyzer
        }


print(generate().__next__())
