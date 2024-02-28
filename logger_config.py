import logging
from logging.handlers import TimedRotatingFileHandler

def configure_logger():
    # 配置TimedRotatingFileHandler
    handler = TimedRotatingFileHandler('mylog.log', when="midnight", interval=1, backupCount=7)

    # 设置日志级别
    handler.setLevel(logging.DEBUG)

    # 配置日志格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # 添加handler到root logger
    logging.getLogger('').addHandler(handler)
