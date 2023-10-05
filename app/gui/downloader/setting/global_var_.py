import threading

from configobj import ConfigObj

from app.common.constantx import FILE_DOWNLOAD_PATH, GLOBAL_VAR_FILE_PATH
from app.gui.downloader.utils import check_proxy

__all__ = ["globals_var", "GlobalVar"]


class GlobalVar:
    """全局配置后续放置在数据库中"""

    _instance_lock = threading.Lock()

    def __init__(self):
        self.config = ConfigObj(GLOBAL_VAR_FILE_PATH, encoding="UTF8")
        if not self.config["globalvars"]["DOWNLOAD_DIRECTORY"]:
            self.config["globalvars"]["DOWNLOAD_DIRECTORY"] = FILE_DOWNLOAD_PATH
        self.DOWNLOAD_DIRECTORY = self.config["globalvars"]["DOWNLOAD_DIRECTORY"]
        self.THREAD = self.config["globalvars"]["THREAD"]
        self.LANGUAGE = self.config["globalvars"]["LANGUAGE"]
        self.THEME = self.config["globalvars"]["THEME"]
        # self.FILENAME = self.config['globalvars']['FILENAME']
        # self.TABLE = self.config['globalvars']['TABLE']
        self.setting_proxy_http = self.config["globalvars"]["PROXY"]
        self.PROXY = check_proxy(self.setting_proxy_http)
        if not self.PROXY:
            self.PROXY = ""

    def __new__(cls, *args, **kwargs):
        if not hasattr(GlobalVar, "_instance"):
            with GlobalVar._instance_lock:
                if not hasattr(GlobalVar, "_instance"):
                    GlobalVar._instance = object.__new__(cls)
        return GlobalVar._instance

    def update_download_directory(self, files_storage):
        self.config["globalvars"]["DOWNLOAD_DIRECTORY"] = files_storage
        self.config.write()
        self.DOWNLOAD_DIRECTORY = files_storage

    def update_threads(self, thread):
        self.config["globalvars"]["THREAD"] = thread
        self.config.write()
        self.THREAD = thread

    def update_languages(self, language):
        self.config["globalvars"]["LANGUAGE"] = language
        self.config.write()
        self.LANGUAGE = language

    def update_themes(self, theme):
        self.config["globalvars"]["THEME"] = theme
        self.config.write()
        self.LANGUAGE = theme

    def update_static(self, path):
        pass
        # self.config['globalvars']['LANGUAGE'] = path
        # self.config.write()
        # self.STATIC = path

    def update_proxy(self, proxy):
        check_proxy(proxy)
        self.config["globalvars"]["PROXY"] = proxy
        self.config.write()


globals_var = GlobalVar()
