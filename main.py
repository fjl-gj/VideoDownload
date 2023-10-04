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

import os
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QApplication

from app.gui.core.json_settings import Settings
from app.gui.downloader.log.log import logger
from app.gui.uis.windows.main_window import UI_MainWindow, SetupMainWindow
from app.gui.uis.windows.main_window.functions_main_window import MainFunctions

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////

# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
# IMPORT PY ONE DARK WINDOWS
# ///////////////////////////////////////////////////////////////
# MAIN WINDOW
# IMPORT PY ONE DARK WIDGETS
# ///////////////////////////////////////////////////////////////
# ADJUST QT FONT DPI FOR HIGHT SCALE AN 4K MONITOR
# ///////////////////////////////////////////////////////////////

os.environ["QT_FONT_DPI"] = "96"


# IF IS 4K MONITOR ENABLE 'os.environ["QT_SCALE_FACTOR"] = "2"'


# MAIN WINDOW
# ///////////////////////////////////////////////////////////////
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items

        # SETUP MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.hide_grips = True  # Show/Hide resize grips
        SetupMainWindow.setup_gui(self)

        # SHOW MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.show()

    # LEFT MENU BTN IS CLICKED
    # Run function when btn is clicked
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////
    def btn_clicked(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # TITLE BAR MENU
        # ///////////////////////////////////////////////////////////////

        # OPEN Home Page
        if btn.objectName() == "btn_home":
            # Select menu
            self.ui.left_menu.select_only_one(btn.objectName())
            MainFunctions.set_page(self, self.ui.load_pages.home_page)

        # OPEN Downloading Page
        if btn.objectName() == "btn_download":
            # Select menu
            self.ui.left_menu.select_only_one(btn.objectName())
            MainFunctions.set_page(self, self.ui.load_pages.download_page)

        if btn.objectName() == "btn_info":
            self.ui.left_menu.select_only_one(btn.objectName())
            MainFunctions.set_page(self, self.ui.load_pages.version_page)

        # OPEN settings Page
        if btn.objectName() == "btn_settings":
            # Select menu
            self.ui.left_menu.select_only_one(btn.objectName())
            MainFunctions.set_page(self, self.ui.load_pages.setting_page)

        # SETTINGS TITLE BAR
        if btn.objectName() == "btn_top_settings":
            self.ui.left_menu.select_only_one(btn.objectName())
            MainFunctions.set_page(self, self.ui.load_pages.setting_page)

            # Get Left Menu Btn
            btn_settings = MainFunctions.get_left_menu_btn(self, "btn_settings")
            btn_settings.set_active_tab(False)

        # DEBUG
        logger.info(f"Button {btn.objectName()}, clicked!")

    # LEFT MENU BTN IS RELEASED
    # Run function when btn is released
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////
    def btn_released(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # DEBUG
        logger.info(f"Button {btn.objectName()}, released!")

    # RESIZE EVENT
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        SetupMainWindow.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        # self.dragPos = event.globalPos()
        self.dragPos = event.globalPosition().toPoint()


# SETTINGS WHEN TO START
# Set the initial class and also additional parameters of the "QApplication" class
# ///////////////////////////////////////////////////////////////
# if __name__ == "__main__":
# APPLICATION
# ///////////////////////////////////////////////////////////////

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#
# sys.path.append(os.path.join(BASE_DIR, 'gui'))
# sys.path.append(os.path.join(BASE_DIR, 'gui'))
# sys.path.append(os.path.join(BASE_DIR, 'gui'))
# sys.path.append(os.path.join(BASE_DIR, 'gui'))

app = QApplication(sys.argv)
app.setWindowIcon(QIcon("icon.ico"))
window = MainWindow()

# print('当前进程的内存使用：', psutil.Process(os.getpid()).memory_info().rss)
# print('当前进程的内存使用：%.4f GB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 / 1024))

# EXEC APP
# ///////////////////////////////////////////////////////////////
sys.exit(app.exec())
