import os
import threading
from gui.downloader.utils import check_proxy
from configobj import ConfigObj

__all__ = ["globals_var"]


class GlobalVar:

    _instance_lock = threading.Lock()

    def __init__(self, file_ini='global_var.ini'):
        self.BASE_DIR = os.path.abspath(os.getcwd())
        self.path = os.path.join(os.path.join(self.BASE_DIR, 'static'), file_ini)
        self.config = ConfigObj(self.path, encoding='UTF8')
        if self.config['globalvars']['DOWNDIRECTORY']:
            self.DOWNDIRECTORY = self.config['globalvars']['DOWNDIRECTORY']
        else:
            self.config['globalvars']['DOWNDIRECTORY'] = os.path.join(os.path.join(self.BASE_DIR, 'static'), 'resource')
            self.DOWNDIRECTORY = f"{os.path.dirname(self.path)}\\resource"
        self.THREAD = self.config['globalvars']['THREAD']
        self.LANGUAGE = self.config['globalvars']['LANGUAGE']
        self.THEME = self.config['globalvars']['THEME']
        self.FILENAME = self.config['globalvars']['FILENAME']
        self.TABLE = self.config['globalvars']['TABLE']
        self.setting_proxy_http = self.config['globalvars']['PROXY']
        self.PROXY = check_proxy(self.setting_proxy_http)
        if not self.PROXY:
            self.PROXY = 'None'

    def __new__(cls, *args, **kwargs):
        if not hasattr(GlobalVar, "_instance"):
            with GlobalVar._instance_lock:
                if not hasattr(GlobalVar, "_instance"):
                    GlobalVar._instance = object.__new__(cls)
        return GlobalVar._instance

    def update_DOWNDIRECTORY(self, files_torage):
        self.config['globalvars']['DOWNDIRECTORY'] = files_torage
        self.config.write()
        self.DOWNDIRECTORY = files_torage

    def update_THREAD(self, thread):
        self.config['globalvars']['THREAD'] = thread
        self.config.write()
        self.THREAD = thread

    def update_LANGUAGE(self, language):
        self.config['globalvars']['LANGUAGE'] = language
        self.config.write()
        self.LANGUAGE = language

    def update_THEME(self, theme):
        self.config['globalvars']['THEME'] = theme
        self.config.write()
        self.LANGUAGE = theme

    def update_STATIC(self, path):
        self.config['globalvars']['LANGUAGE'] = path
        self.config.write()
        self.STATIC = path

    def update_PROXY(self, proxy):
        self.config['globalvars']['PROXY'] = proxy
        self.config.write()


globals_var = GlobalVar()
