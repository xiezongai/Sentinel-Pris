
import json
import logging
import traceback
import uuid
from peewee import OperationalError
from database.model.action_log_model import ActionLogModel

info_logger = logging.getLogger("info")
error_logger = logging.getLogger("error")
warning_logger = logging.getLogger("warning")

class ActionLogDAO(object):

    @staticmethod
    def log_action(user_id, action_type, action_name, action_status, action_msg):
        try:
            ActionLogModel.create(
                _id = str(uuid.uuid4()),
                action_name = action_name,
                action_type = action_type,
                action_status = action_status,
                action_msg = action_msg,
                user_id = user_id
            )
        except OperationalError as operational_e:
            error_logger.error("记录Request到数据库时发生连接数据库错误, %s,%s", str(operational_e), traceback.format_exc(), extra={"host": 'localhost'})
            raise BaseException("连接数据库发生错误")
        except:
            error_logger.error("记录Request到数据库时发生其他错误, %s", traceback.format_exc(), extra={"host": 'localhost'})
            raise BaseException("连接数据库发生错误")
    
    