import os.path

from app.common.constantx import FILE_DOWNLOAD_PATH, LOG_PATH, MODEL_DB_PATH

__all__ = ["preload"]


class PreLoad:
    DIRECT_LIST = [FILE_DOWNLOAD_PATH, LOG_PATH, MODEL_DB_PATH]

    def __init__(self):
        self.check_and_create_directory()

    def check_and_create_directory(self):
        for dir_ in self.DIRECT_LIST:
            print(dir_)
            if os.path.exists(dir_):
                continue
            os.mkdir(dir_)


preload = PreLoad()
