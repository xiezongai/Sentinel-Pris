"""
TODO : dialogs 表修改过，很多方法都要改
"""
import logging
import traceback
import datetime
from peewee import OperationalError
from database.model.dialogs_model import Dialogs
import time
import json
from peewee import fn
import traceback

from datetime import datetime, timedelta

info_logger = logging.getLogger("info")
error_logger = logging.getLogger("error")
warning_logger = logging.getLogger("warning")


class DialogsDAO(object):
        
    @staticmethod
    def convert_datetime_to_timestamp(input_datetime):
        # d = datetime.datetime.strptime(str(input_datetime), "%Y-%m-%d %H:%M:%S")
        t = input_datetime.timetuple()
        timeStamp = int(time.mktime(t))
        timeStamp = float(str(timeStamp) + str("%06d" % input_datetime.microsecond)) / 1000000
        return timeStamp

    @staticmethod
    def add_s2t_result_to_dialog(id, transcripts, emotion, silence, interruption):
        try:
            dialogs = (Dialogs.select(Dialogs.id).where(Dialogs.id==id)).execute()
            if len(list(dialogs)) == 1:
                (Dialogs.update(
                    transcripts=transcripts,
                    emotion=emotion,
                    silence=silence,
                    interruption=interruption
                ).where(Dialogs.id==id)).execute()
                return True
            else:
                raise Exception("没有这个ID")
        except Exception as e:
            error_logger.error("将新的Dialog数据写入的时候错误, %s, Traceback: %s",str(e) , traceback.format_exc(), extra={"host": 'localhost'})
            return False

    @staticmethod
    def update_status_by_session_id(session_id, new_status):
        try:
            print(session_id)
            dialogs = (Dialogs.select(Dialogs.id).where(Dialogs.session_id==session_id)).execute()
            print("Found " + str(len(list(dialogs))) + " Dialogs")
            if len(list(dialogs)) != 0:
                (Dialogs.update(status=new_status).where(Dialogs.session_id==session_id)).execute()
                return True
            else:
                raise Exception("没有这个SessionID")
        except Exception as e:
            error_logger.error("将新的Dialog数据写入的时候错误, %s, Traceback: %s",str(e) , traceback.format_exc(), extra={"host": 'localhost'})
            return False

    @staticmethod
    def update_status_by_id(id, new_status):
        try:
            dialogs = (Dialogs.select(Dialogs.id).where(Dialogs.id==id)).execute()
            if len(list(dialogs)) == 1:
                Dialogs.update(status=new_status).where(Dialogs.id==id)
                return True
            else:
                raise Exception("没有这个ID")
        except Exception as e:
            error_logger.error("将新的Dialog数据写入的时候错误, %s, Traceback: %s",str(e) , traceback.format_exc(), extra={"host": 'localhost'})
            return False

    @staticmethod
    def import_dialog_from_info(id, call_id, caller_no, callee_no, begin_time, end_time, session_id):
        try:
            new_dialog=Dialogs.create(
                id=id,
                call_id=call_id,
                caller_no=caller_no,
                callee_no=callee_no,
                begin_time=begin_time,
                end_time=end_time,
                session_id = session_id,
                status = 0
            )
            if new_dialog.id ==id:
                return True
            else:
                raise Exception("无法创建一个新的Dialog记录，需要检查传入的所有参数, 创建记录的输出结果是 %s", str(locals()))
        except Exception as e:
            error_logger.error("将新的Dialog数据写入的时候错误, %s, Traceback: %s",str(e) , traceback.format_exc(), extra={"host": 'localhost'})
            return False

    @staticmethod
    def load_dialogs_by_session_id(session_id):
        try:
            dialogs=(Dialogs.select().where(Dialogs.session_id==session_id))
            return dialogs
        except Exception as e:
            error_logger.error("将新的Dialog数据写入的时候错误, %s, Traceback: %s",str(e) , traceback.format_exc(), extra={"host": 'localhost'})
            return False 

    @staticmethod
    def load_dialogs(start_time_s, end_time_s):
        """
        返回对应时间段内的对话
        params start_time_s:str,2018-09-13 00:00:00
        params end_time_s:str,2018-09-14 00:00:00
        """
        start_time = datetime.strptime(start_time_s, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(end_time_s, "%Y-%m-%d %H:%M:%S")
        try:
            dialogs = (Dialogs.select().where((Dialogs.begin_time >= start_time) & (Dialogs.begin_time <= end_time))).execute()
            converted_dialogs = []
            for dialog in dialogs:
                converted_dialogs.append({
                    "id": dialog.id,
                    "call_id": dialog.call_id,
                    "caller_no": dialog.caller_no,
                    "callee_no": dialog.callee_no,
                    "begin_time": dialog.begin_time,  # datetime
                    "end_time": dialog.end_time,  # datetime
                    "transcripts": [] if dialog.transcripts=='' else json.loads(dialog.transcripts, encoding='utf-8'),
                    "emotion": dialog.emotion,
                    "silence_max":dialog.silence_max,
                    "silence_total":dialog.silence_total,
                    "interruption": dialog.interruption,
                    "interruption_status": dialog.interruption_status,
                    "status": dialog.status,
                    "session_id" : dialog.session_id
                })
            return converted_dialogs
        except:
            error_logger.error("从数据库读取对话时发生其他错误, %s", traceback.format_exc(), extra={"host": 'localhost'})
            raise BaseException("从数据库读取对话时发生其他错误")

    @staticmethod
    def upload_audio_to_info(call_id, session_id):
        '''
        @Description: 用户上传一个对应的语音文件到流水记录后，系统会根据用户提供的callid和session_id更新这条记录状态，通常是从0（Dialog收到流水信息，还没有收到语音文件）到1（Dialog收到语音信息） 
        '''
        try: 
            fetch_query = (Dialogs.select(Dialogs.id).where((Dialogs.call_id==call_id) & (Dialogs.session_id==session_id)))
            fetch_query.execute()
            if len(fetch_query) == 1:
                target_id=fetch_query[0].id
                update_query = (Dialogs.update(status=1).where(Dialogs.id==target_id))
                update_query.execute()
                return target_id
            else:
                raise Exception("无法根据call_id和session_id找到需要更新的record")
        except Exception as e:
            error_logger.error("无法更新 %s Dialog的状态, 原因：%s, TraceBack: %s",str(call_id), str(e), traceback.format_exc(), extra={"host": "localhost"})
            return False

    @staticmethod
    def load_dialog_by_id(dialog_id):
        try:
            dialogs = (Dialogs.select().where(Dialogs.id == dialog_id)).execute()
            if len(dialogs) == 1:
                return {
                    "id": dialogs[0].id,
                    "call_id": dialogs[0].call_id,
                    "caller_no": dialogs[0].caller_no,
                    "callee_no": dialogs[0].callee_no,
                    "begin_time": dialogs[0].begin_time,
                    "end_time": dialogs[0].end_time,
                    "transcripts": [] if dialogs[0].transcripts=='' else json.loads(dialogs[0].transcripts, encoding='utf-8'),
                    "emotion": dialogs[0].emotion,
                    "silence":dialogs[0].silence,
                    "interruption": dialogs[0].interruption,
                    "status": dialogs[0].status,
                    "session_id" : dialogs[0].session_id
                }
        except:
            error_logger.error("从数据库读取对话时发生其他错误, %s", traceback.format_exc(), extra={"host": 'localhost'})
            raise BaseException("从数据库读取对话时发生其他错误")

    @staticmethod
    def convert_dialogs_repeat_call_format(dialogs):
        """
        将peewee取出的对话转化为以下格式：
        {"call_id": {"content":[("user", "start_time", "end_time", "你摸着自己良心我有说错吗？"),
                                          ("customer_service", "start_time", "end_time", "你是变态啊")],
                     "user_id": ""
                     "time": datetime}
        }
        """
        result = {}
        for dialog in dialogs:
            dialog_id = dialog.dialog_id
            result[dialog_id] = {"content": [], "user_id": dialog.user_id, "time": dialog.dialog_start_time}

            for row in dialog.content.split('\n'):
                try:
                    target, start_time, end_time, sentence = row.split('\t')
                    result[dialog_id]["content"].append(
                        ("user" if target == '0' else "customer_service", start_time, end_time, sentence)
                    )
                except Exception:
                    pass
        return result

    @staticmethod
    def view_dialogs(start_time_s, end_time_s, page_num, page_size):
        start_time = datetime.strptime(start_time_s + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(end_time_s + " 00:00:00", "%Y-%m-%d %H:%M:%S") + timedelta(days=1)
        try:
            dialogs = (Dialogs.select()
            .where(
                (Dialogs.created_at >= start_time) & 
                (Dialogs.created_at <= end_time))
            .order_by(Dialogs.created_at)
            .paginate(page_num, page_size)
            ).execute()
            converted_dialogs = []
            for dialog in dialogs:
                converted_dialogs.append ({
                    "id": dialog.id,
                    "call_id": dialog.call_id,
                    "caller_no": dialog.caller_no,
                    "callee_no": dialog.callee_no,
                    "begin_time": str(dialog.begin_time),
                    "end_time": str(dialog.end_time),
                    "status": dialog.status,
                    "is_manual_rated": dialog.is_manual_rated,
                    "manual_score": dialog.manual_score,
                    "machine_score": dialog.machine_score,
                    "created_at": datetime.strftime(dialog.created_at, "%Y-%m-%d %H:%M:%S")
                })
            return converted_dialogs
        except:
            error_logger.error("从数据库读取对话时发生其他错误, %s", traceback.format_exc(), extra={"host": 'localhost'})
            raise BaseException("从数据库读取对话时发生其他错误")

    @staticmethod
    def view_dialogs_advance(start_time_s, end_time_s, page_num, page_size, filter_items, sort_items):
        start_time = datetime.strptime(start_time_s + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(end_time_s + " 00:00:00", "%Y-%m-%d %H:%M:%S") + timedelta(days=1)
        filter_condi = [True, False]
        if 'is_manual_rated' in filter_items:
            if filter_items['is_manual_rated'] == 1:
                #Print all filtered human rated results
                filter_condi[1] = True 
            if filter_items['is_manual_rated'] == -1:
                filter_condi[0] = False 
        try:
            print 
            dialogs = None
            if sort_items is not None and "created_at" in sort_items and sort_items["created_at"] == "descend":
                dialogs = (Dialogs.select()
                .where(
                    (Dialogs.created_at >= start_time) & 
                    (Dialogs.created_at <= end_time) &
                    ((Dialogs.is_manual_rated == filter_condi[0])|(Dialogs.is_manual_rated == filter_condi[1]))
                )
                .order_by(Dialogs.created_at.desc())
                .paginate(page_num, page_size)
                ).execute()
            elif sort_items is not None and "created_at" in sort_items and sort_items["created_at"] == "ascend":
                dialogs = (Dialogs.select()
                .where(
                    (Dialogs.created_at >= start_time) & 
                    (Dialogs.created_at <= end_time) &
                    ((Dialogs.is_manual_rated == filter_condi[0])|(Dialogs.is_manual_rated == filter_condi[1]))
                )
                .order_by(Dialogs.created_at)
                .paginate(page_num, page_size)
                ).execute()
            elif sort_items is not None and "manual_score" in sort_items and sort_items["manual_score"] == "descend":
                dialogs = (Dialogs.select()
                .where(
                    (Dialogs.created_at >= start_time) & 
                    (Dialogs.created_at <= end_time)&
                    ((Dialogs.is_manual_rated == filter_condi[0])|(Dialogs.is_manual_rated == filter_condi[1]))
                )
                .order_by(Dialogs.manual_score.desc())
                .paginate(page_num, page_size)
                ).execute()
            elif sort_items is not None and "manual_score" in sort_items and sort_items["manual_score"] == "ascend":
                dialogs = (Dialogs.select()
                .where(
                    (Dialogs.created_at >= start_time) & 
                    (Dialogs.created_at <= end_time)&
                    ((Dialogs.is_manual_rated == filter_condi[0])|(Dialogs.is_manual_rated == filter_condi[1]))
                )
                .order_by(Dialogs.manual_score)
                .paginate(page_num, page_size)
                ).execute()
            elif sort_items is not None and "machine_score" in sort_items and sort_items["machine_score"] == "descend":
                dialogs = (Dialogs.select()
                .where(
                    (Dialogs.created_at >= start_time) & 
                    (Dialogs.created_at <= end_time)&
                    ((Dialogs.is_manual_rated == filter_condi[0])|(Dialogs.is_manual_rated == filter_condi[1]))
                )
                .order_by(Dialogs.machine_score.desc())
                .paginate(page_num, page_size)
                ).execute()
            elif sort_items is not None and "machine_score" in sort_items and sort_items["machine_score"] == "ascend":
                dialogs = (Dialogs.select()
                .where(
                    (Dialogs.created_at >= start_time) & 
                    (Dialogs.created_at <= end_time)&
                    ((Dialogs.is_manual_rated == filter_condi[0])|(Dialogs.is_manual_rated == filter_condi[1]))
                )
                .order_by(Dialogs.machine_score)
                .paginate(page_num, page_size)
                ).execute()
            else:
                dialogs = (Dialogs.select()
                .where(
                    (Dialogs.created_at >= start_time) & 
                    (Dialogs.created_at <= end_time)&
                    ((Dialogs.is_manual_rated == filter_condi[0])|(Dialogs.is_manual_rated == filter_condi[1]))
                )
                .order_by(Dialogs.created_at)
                .paginate(page_num, page_size)
                ).execute()
            converted_dialogs = []
            for dialog in dialogs:
                converted_dialogs.append ({
                    "id": dialog.id,
                    "call_id": dialog.call_id,
                    "caller_no": dialog.caller_no,
                    "callee_no": dialog.callee_no,
                    "begin_time": str(dialog.begin_time),
                    "end_time": str(dialog.end_time),
                    "status": dialog.status,
                    "is_manual_rated": dialog.is_manual_rated,
                    "manual_score": dialog.manual_score,
                    "machine_score": dialog.machine_score,
                    "created_at": datetime.strftime(dialog.created_at, "%Y-%m-%d %H:%M:%S")
                })
            return converted_dialogs
        except:
            error_logger.error("从数据库读取对话时发生其他错误, %s", traceback.format_exc(), extra={"host": 'localhost'})
            raise BaseException("从数据库读取对话时发生其他错误")

    @staticmethod
    def view_dialog_by_id(dialog_id):
        dialog = (Dialogs.select().where(Dialogs.id==dialog_id)).execute()
        if len(dialog) == 1:
            return {
                "id": dialog[0].id,
                "call_id": dialog[0].call_id,
                "caller_no": dialog[0].caller_no,
                "callee_no": dialog[0].callee_no,
                "begin_time": str(dialog[0].begin_time),
                "end_time": str(dialog[0].end_time),
                "status": dialog[0].status,
                "transcripts": [] if dialog[0].transcripts=='' else json.loads(dialog[0].transcripts, encoding='utf-8'),
                "is_manual_rated": dialog[0].is_manual_rated,
                "manual_rating": {} if dialog[0].is_manual_rated is False else json.loads(dialog[0].manual_rating, encoding='utf-8'),
                "manual_score": dialog[0].manual_score,
                "machine_score": dialog[0].machine_score,
                "created_at": datetime.strftime(dialog[0].created_at, "%Y-%m-%d %H:%M:%S"),
                "session_id": dialog[0].session_id
            }
        else:
            raise Exception("Cannot find dialog with given id")
    
    @staticmethod
    def update_dialog_with_manual_rating(dialog_id, manual_rating, manual_score):
        dialog = (Dialogs.select().where(Dialogs.id==dialog_id)).execute()
        if len(dialog) == 1:
            (Dialogs.update(
                is_manual_rated=True,
                manual_score = manual_score,
                manual_rating = json.dumps(manual_rating, ensure_ascii=False)
            ).where(Dialogs.id == dialog_id)).execute()
            return True
        else:
            raise Exception("Cannot find dialog with given id")

    @staticmethod
    def count_dialogs_between_time(start_time_s, end_time_s):
        start_time = datetime.strptime(start_time_s + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(end_time_s + " 00:00:00", "%Y-%m-%d %H:%M:%S") + timedelta(days=1)
        count = Dialogs.select(fn.Count(Dialogs.id)).where((Dialogs.created_at >= start_time) & (Dialogs.created_at <= end_time)).scalar()
        return count

    @staticmethod
    def count_dialogs_between_time_advance(start_time_s, end_time_s, filter_items):
        start_time = datetime.strptime(start_time_s + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(end_time_s + " 00:00:00", "%Y-%m-%d %H:%M:%S") + timedelta(days=1)
        filter_condi = [True, False]
        if 'is_manual_rated' in filter_items:
            if filter_items['is_manual_rated'] == 1:
                #Print all filtered human rated results
                filter_condi[1] = True 
            if filter_items['is_manual_rated'] == -1:
                filter_condi[0] = False 
        try:
            count = Dialogs.select(fn.Count(Dialogs.id)).where(
                (Dialogs.created_at >= start_time) & 
                (Dialogs.created_at <= end_time) &
                ((Dialogs.is_manual_rated == filter_condi[0])|(Dialogs.is_manual_rated == filter_condi[1]))
            ).scalar()
            return count
        except:
            error_logger.error("从数据库读取对话时发生其他错误, %s", traceback.format_exc(), extra={"host": 'localhost'})
            raise BaseException("从数据库读取对话时发生其他错误")
