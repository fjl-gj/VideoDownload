# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
import json
import os

# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from app.common.constantx import THEMES_PATH
from app.gui.core.json_settings import Settings
# APP THEMES
# ///////////////////////////////////////////////////////////////
from app.gui.downloader.log.log import logger
from app.gui.downloader.setting.global_var_ import globals_var

THEMES_FILE_NAME = f"{globals_var.THEME}.json"
THEMES_FILE_PATH = os.path.join(THEMES_PATH, THEMES_FILE_NAME)


class Themes(object):
    # LOAD SETTINGS
    # ///////////////////////////////////////////////////////////////
    setup_settings = Settings()
    _settings = setup_settings.items

    settings_path = THEMES_FILE_PATH
    if not os.path.isfile(settings_path):
        logger.error(
            f"WARNING: {_settings['theme_name']}.json not found! "
            f"Please check in the folder {settings_path}"
        )

    # INIT SETTINGS
    # ///////////////////////////////////////////////////////////////
    def __init__(self):
        super(Themes, self).__init__()

        # DICTIONARY WITH SETTINGS
        self.items = {}

        # DESERIALIZE
        self.deserialize()

    # SERIALIZE JSON
    # ///////////////////////////////////////////////////////////////
    def serialize(self):
        # WRITE JSON FILE
        with open(self.settings_path, "w", encoding="utf-8") as write:
            json.dump(self.items, write, indent=4)

    # DESERIALIZE JSON
    # ///////////////////////////////////////////////////////////////
    def deserialize(self):
        # READ JSON FILE
        with open(self.settings_path, "r", encoding="utf-8") as reader:
            settings = json.loads(reader.read())
            self.items = settings

    @property
    def app_color(self):
        return self.items["app_color"]

    @property
    def app_font(self):
        return self.items["font"]
