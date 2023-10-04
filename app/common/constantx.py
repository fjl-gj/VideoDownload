import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# app
APP_PATH = os.path.join(BASE_DIR, "app")

# themes
THEMES_PATH = os.path.join(BASE_DIR, "themes")

# conf
CONF_PATH = os.path.join(BASE_DIR, "conf")
CONF_FILE_NAME = "settings.json"
CONF_FILE_PATH = os.path.join(CONF_PATH, CONF_FILE_NAME)

# global_var.ini
GLOBAL_VAR_FILE_NAME = "global_var.ini"
GLOBAL_VAR_FILE_PATH = os.path.join(CONF_PATH, GLOBAL_VAR_FILE_NAME)

# resource download path
FILE_DOWNLOAD_PATH = os.path.join(BASE_DIR, "resources")

# static resource
STATIC_PATH = os.path.join(BASE_DIR, "static")

# log
LOG_PATH = os.path.join(BASE_DIR, "log")
LOG_FILE_NAME = "video_download.log"
LOG_FILE_PATH = os.path.join(LOG_PATH, LOG_FILE_NAME)
