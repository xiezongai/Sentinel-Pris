import logging
import traceback
from database.model.session_model import SessionModel

info_logger = logging.getLogger("info")
error_logger = logging.getLogger("error")
warning_logger = logging.getLogger("warning")

class SessionDAO(object):

    @staticmethod
    def create_new_session(session_id,user_id):
        try:
            SessionModel.create(
                id=session_id,
                user_id= user_id
            )
            return id
        except Exception as e:
            error_logger.error("无法创建一个新的Session, %s", traceback.format_exc(), extra={"host": 'localhost'})
            return False
    