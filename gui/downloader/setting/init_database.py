import sqlite3
from functools import wraps
from gui.downloader.log.log import logger

from gui.downloader.setting.global_var_ import globals_var

"""
download_status : 0  finished     1  downloading        2 pause
is_delete       : 0  delete       1  not delete
"""


def singleton(cls):
    _instance = {}

    def _singleton_new(func):
        @wraps(func)
        def _(*args, **kwargs):
            # 先判断这个类有没有对象
            if cls not in _instance:
                obj = func(*args, **kwargs)  # 创建一个对象,并保存到字典当中
                _instance[cls] = (obj, True)
            else:
                obj, _ = _instance[cls]
                _instance[cls] = (obj, False)
            # 将实例对象返回
            return obj

        return _

    def _singleton_init(func):
        @wraps(func)
        def _(*args, **kwargs):
            flag = True
            if cls in _instance:
                obj, flag = _instance[cls]
            if flag:
                func(*args, **kwargs)

        return _

    __new__ = cls.__new__
    __init__ = cls.__init__

    @_singleton_new
    def _new_(cls_, *args, **kwargs):
        if hasattr(__new__, "__code__"):
            o = __new__(cls_, *args, **kwargs)
        else:
            o = __new__(cls_)
        return o

    @_singleton_init
    def _init_(self, *args, **kwargs):
        __init__(self, *args, **kwargs)

    # 替换原类的__new__和__init__方法
    cls.__new__ = _new_
    cls.__init__ = _init_
    return cls


@singleton
class SqlLite:
    """initialized database"""

    def __init__(self):
        self.db_file = f'{globals_var.BASE_DIR}\\static\\{globals_var.FILENAME}.db'
        is_create_table = self.check_table()
        if not is_create_table:
            self.create_table()
            logger.info("初始化成功")
        else:
            logger.info("已完成初始化")

    def init_close_database(func):
        def wrapper(self, *args, **kwargs):
            self.con = sqlite3.connect(self.db_file)
            self.cur = self.con.cursor()
            result = func(self, *args, **kwargs)
            self.con.commit()
            self.cur.close()
            self.con.close()
            return result
        return wrapper

    @init_close_database
    def check_table(self):
        result = self.cur.execute(f'''PRAGMA table_info({globals_var.TABLE});''')
        return True if result.fetchone() else False

    @init_close_database
    def create_table(self):
        self.cur.executescript(f'''
        PRAGMA foreign_keys = false;
        
        -- ----------------------------
        -- Table structure for video_download
        -- ----------------------------
        DROP TABLE IF EXISTS {globals_var.TABLE};
        CREATE TABLE {globals_var.TABLE} (
          "id" integer NOT NULL ON CONFLICT IGNORE COLLATE NOCASE,
          "title" TEXT NOT NULL,
          "uploader" TEXT NOT NULL,
          "duration" TEXT NOT NULL,
          "quality" TEXT NOT NULL,
          "file_type" TEXT NOT NULL,
          "file_size" TEXT NOT NULL,
          "download_status" integer NOT NULL,
          "is_delete" integer,
          "create_time" TEXT NOT NULL,
          "update_time" TEXT,
          "format_id" INTEGER NOT NULL,
          "url_id" TEXT NOT NULL,
          "webpage_url" TEXT NOT NULL,
          "down_url" TEXT,
          "down_file_size" integer,
          "size" integer,
          "down_percentage" integer,
          "file_path_name"  TEXT,
          PRIMARY KEY ("id"),
          CONSTRAINT "id" UNIQUE ("id" ASC) ON CONFLICT IGNORE
        );
        
        -- ----------------------------
        -- Indexes structure for table video_download
        -- ----------------------------
        CREATE INDEX "video_download_format_id"
        ON "video_download" (
          "format_id" ASC
        );
        CREATE INDEX "video_download_url_id"
        ON "video_download" (
          "url_id" ASC
        );
        
        PRAGMA foreign_keys = true;''')

    def dict_factory(self, cursor, row):
        d = {}
        for index, col in enumerate(cursor.description):
            d[col[0]] = row[index]
        return d

    def return_databases_connect(self):
        con = sqlite3.connect(self.db_file)
        con.row_factory = self.dict_factory
        return con


lite = SqlLite()
