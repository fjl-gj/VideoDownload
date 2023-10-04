import os

from app.gui.downloader.setting.global_var_ import globals_var

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# app
APP_PATH = os.path.join(BASE_DIR, "app")

# themes
THEMES_PATH = os.path.join(APP_PATH, "themes")
THEMES_FILE_NAME = f"{globals_var.THEME}.json"
THEMES_FILE_PATH = os.path.join(THEMES_PATH, THEMES_FILE_NAME)

# conf
CONF_PATH = os.path.join(BASE_DIR, "conf")
CONF_FILE_NAME = "settings.json"
CONF_FILE_PATH = os.path.join(CONF_PATH, CONF_FILE_NAME)
