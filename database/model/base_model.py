import datetime
import logging
import os
import socket
import sys
import traceback

from peewee import *

MYSQL_PORT=None
MYSQL_USER=None
MYSQL_PSWD=None
MYSQL_HOST=None
db=None

host_addr = socket.gethostname()
info_logger = logging.getLogger("info")
error_logger = logging.getLogger("error")
warning_logger = logging.getLogger("warning")

try:
	MYSQL_PORT = int(os.environ["MYSQL_PORT"])
	MYSQL_USER = os.environ["MYSQL_USER"]
	MYSQL_HOST = os.environ["MYSQL_HOST"]
	MYSQL_PSWD = os.environ["MYSQL_PSWD"]
except KeyError as e:
	warning_logger.warning("数据库初始化读取环境参数失败，使用默认参数: %s , Traceback信息: %s", str(e), traceback.format_exc(),  extra={"host": host_addr})
	MYSQL_PORT = 3306
	MYSQL_USER = "helic"
	MYSQL_PSWD = "root1234"
	MYSQL_HOST = "localhost"
except Exception as e:
	error_logger.error("数据库初始化错误: %s, %s", str(e), traceback.format_exc(),  extra={"host": host_addr})
	exit()

try:
    db = MySQLDatabase('ellison', user=MYSQL_USER, password=MYSQL_PSWD, host=MYSQL_HOST, port=MYSQL_PORT, charset='utf8mb4')
except Exception as e:
	error_logger.error("数据库读取失败: %s, %s", str(e), traceback.format_exc(),  extra={"host": host_addr})
	exit()

class BaseModel(Model):
	class Meta:
		database = db
