import logging
import os
from logging.handlers import TimedRotatingFileHandler

from app.common.constantx import LOG_PATH, LOG_FILE_NAME


class LogOptions:
    interval = 1
    backup_count = 5
    console_output_level = "INFO"
    file_output_level = "INFO"


class Logger(object):
    def __init__(self, logger_name="log"):
        self.logger = logging.getLogger(logger_name)
        logging.root.setLevel(logging.NOTSET)
        # 最多存放日志的数量和间隔时间创建文件
        self.backup_count = LogOptions.backup_count
        self.interval = LogOptions.interval
        # 日志输出级别
        self.console_output_level = LogOptions.console_output_level
        self.file_output_level = LogOptions.file_output_level

        # 日志输出格式
        self.formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    def get_logger(self):
        """在logger中添加日志句柄并返回，如果logger已有句柄，则直接返回"""
        if not self.logger.handlers:  # 避免重复日志
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)
            console_handler.setLevel(self.console_output_level)
            self.logger.addHandler(console_handler)

            # 每天重新创建一个日志文件，最多保留backup_count份
            file_handler = TimedRotatingFileHandler(
                filename=os.path.join(LOG_PATH, LOG_FILE_NAME),
                when="D",
                interval=self.interval,
                backupCount=self.backup_count,
                delay=True,
                encoding="utf-8",
            )
            file_handler.setFormatter(self.formatter)
            file_handler.setLevel(self.file_output_level)
            self.logger.addHandler(file_handler)
        return self.logger


logger = Logger().get_logger()
