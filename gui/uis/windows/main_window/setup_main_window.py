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

# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
# IMPORT THEME COLORS
# ///////////////////////////////////////////////////////////////
# IMPORT PY ONE DARK WIDGETS
# ///////////////////////////////////////////////////////////////
# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////

# MAIN FUNCTIONS
# ///////////////////////////////////////////////////////////////

from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QClipboard

from .functions_main_window import *
# PY WINDOW
# ///////////////////////////////////////////////////////////////
from .page_ui.download_page import PyDownloadPage
from .page_ui.home_page import PyHomePage, PyLinkParse
from .page_ui.setting_page import PySettingsPage


# LOAD UI MAIN
# ///////////////////////////////////////////////////////////////


class SetupMainWindow:
    def __init__ (self):
        super().__init__()
        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

    # ADD LEFT MENUS
    # ///////////////////////////////////////////////////////////////
    add_left_menus = [
        {
            "btn_icon": "icon_home.svg",
            "btn_id": "btn_home",
            "btn_text": "Home",
            "btn_tooltip": "Home page",
            "show_top": True,
            "is_active": True
        },
        {
            "btn_icon": "icon_download.svg",
            "btn_id": "btn_download",
            "btn_text": "Download",
            "btn_tooltip": "Download page",
            "show_top": True,
            "is_active": False
        },
        {
            "btn_icon": "icon_info.svg",
            "btn_id": "btn_info",
            "btn_text": "Info",
            "btn_tooltip": "Info page",
            "show_top": False,
            "is_active": False
        },
        {
            "btn_icon": "icon_settings.svg",
            "btn_id": "btn_settings",
            "btn_text": "Settings",
            "btn_tooltip": "Settings page",
            "show_top": False,
            "is_active": False
        }
    ]

    # ADD TITLE BAR MENUS
    # ///////////////////////////////////////////////////////////////
    add_title_bar_menus = [
        {
            "btn_icon": "icon_settings.svg",
            "btn_id": "btn_top_settings",
            "btn_tooltip": "Top settings",
            "is_active": False
        }
    ]

    # SETUP CUSTOM BTNs OF CUSTOM WIDGETS
    # Get sender() function when btn is clicked
    # ///////////////////////////////////////////////////////////////
    def setup_btns (self):
        if self.ui.title_bar.sender() is not None:
            return self.ui.title_bar.sender()
        elif self.ui.left_menu.sender() is not None:
            return self.ui.left_menu.sender()
        # elif self.ui.left_column.sender() is not None:
        #     return self.ui.left_column.sender()

    # SETUP MAIN WINDOW WITH CUSTOM PARAMETERS
    # ///////////////////////////////////////////////////////////////
    def setup_gui (self):
        # APP TITLE
        # ///////////////////////////////////////////////////////////////
        self.setWindowTitle(self.settings["app_name"])

        # REMOVE TITLE BAR
        # ///////////////////////////////////////////////////////////////
        if self.settings["custom_title_bar"]:
            self.setWindowFlag(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)

        # ADD GRIPS
        # ///////////////////////////////////////////////////////////////
        if self.settings["custom_title_bar"]:
            self.left_grip = PyGrips(self, "left", self.hide_grips)
            self.right_grip = PyGrips(self, "right", self.hide_grips)
            self.top_grip = PyGrips(self, "top", self.hide_grips)
            self.bottom_grip = PyGrips(self, "bottom", self.hide_grips)
            self.top_left_grip = PyGrips(self, "top_left", self.hide_grips)
            self.top_right_grip = PyGrips(self, "top_right", self.hide_grips)
            self.bottom_left_grip = PyGrips(self, "bottom_left", self.hide_grips)
            self.bottom_right_grip = PyGrips(self, "bottom_right", self.hide_grips)

        # LEFT MENUS / GET SIGNALS WHEN LEFT MENU BTN IS CLICKED / RELEASED
        # ///////////////////////////////////////////////////////////////
        # ADD MENUS
        self.ui.left_menu.add_menus(SetupMainWindow.add_left_menus)

        # SET SIGNALS
        self.ui.left_menu.clicked.connect(self.btn_clicked)
        self.ui.left_menu.released.connect(self.btn_released)

        # TITLE BAR / ADD EXTRA BUTTONS
        # ///////////////////////////////////////////////////////////////
        # ADD MENUS
        self.ui.title_bar.add_menus(SetupMainWindow.add_title_bar_menus)

        # SET SIGNALS
        self.ui.title_bar.clicked.connect(self.btn_clicked)
        self.ui.title_bar.released.connect(self.btn_released)

        # ADD Title
        if self.settings["custom_title_bar"]:
            self.ui.title_bar.set_title(self.settings["app_name"])
        else:
            self.ui.title_bar.set_title("Welcome to PyOneDark")

        # LEFT COLUMN SET SIGNALS
        # ///////////////////////////////////////////////////////////////
        # self.ui.left_column.clicked.connect(self.btn_clicked)
        # self.ui.left_column.released.connect(self.btn_released)

        # SET INITIAL PAGE / SET LEFT AND RIGHT COLUMN MENUS
        # ///////////////////////////////////////////////////////////////
        MainFunctions.set_page(self, self.ui.load_pages.home_page)
        # MainFunctions.set_left_column_menu(
        #     self,
        #     menu=self.ui.left_column.menus.menu_1,
        #     title="Settings Left Column",
        #     icon_path=Functions.set_svg_icon("icon_settings.svg")
        # )
        MainFunctions.set_right_column_menu(self, self.ui.right_column.menu_1)

        # ///////////////////////////////////////////////////////////////
        # EXAMPLE CUSTOM WIDGETS
        # Here are added the custom widgets to pages and columns that
        # were created using Qt Designer.
        # This is just an example and should be deleted when creating
        # your application.
        #
        # OBJECTS FOR LOAD PAGES, LEFT AND RIGHT COLUMNS
        # You can access objects inside Qt Designer projects using
        # the objects below:
        #
        # <OBJECTS>
        # LEFT COLUMN: self.ui.left_column.menus
        # RIGHT COLUMN: self.ui.right_column
        # LOAD PAGES: self.ui.load_pages
        # </OBJECTS>
        # ///////////////////////////////////////////////////////////////

        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items

        # LOAD THEME COLOR
        # ///////////////////////////////////////////////////////////////
        themes = Themes()
        self.themes = themes.items

        # LEFT COLUMN
        # ///////////////////////////////////////////////////////////////
        # Home Page
        # ///////////////////////////////////////////////////////////////
        # Signal
        def download_list (result, download_num, formats, sql_id):
            self.download_page.add_download_item(result, download_num, formats, sql_id)

        def show_child_window (resule):
            if self.home_page.child_exsit:
                self.child_widget.close()
            self.child_widget = PyLinkParse(self.ui, resule)
            logger.info('loading child page')
            self.home_page.add_video_table(self.child_widget)
            self.home_page.child_exsit = 1
            self.child_widget.download_action.connect(download_list)
            # self.child_widget.download_data_button.clicked.connect(self.child_widget.ready_download_data)

        def on_clipboard_change ():
            # task = ThreadPoolExecutor(max_workers=2)
            mime_data = self.clipboard.mimeData()
            clipboard_text = mime_data.text().strip()
            link = self.home_page.home_link_input.text()
            if clipboard_text:
                logger.info(f'{clipboard_text}, {link}')
                if link == clipboard_text:
                    return False
                else:
                    if clipboard_text.startswith('http', 0):
                        action_clipboard(mime_data)

        # @run_in_thread_pool()
        def action_clipboard (mime_data):
            self.home_page.home_link_input.setText(mime_data.text())
            self.home_page.child_window_and_link_parem()
            self.clipboard.clear(QClipboard.Clipboard)

        self.home_page = PyHomePage(self.ui)
        self.clipboard = QtWidgets.QApplication.clipboard()
        self.clipboard.dataChanged.connect(on_clipboard_change)
        logger.info('loading home page')
        self.child_widget = PyLinkParse(self.ui, [])
        self.home_page.child_si.connect(show_child_window)
        self.ui.load_pages.home_page_all_config.addWidget(self.home_page)
        self.ui.load_pages.home_page_all_config.addWidget(self.child_widget)
        self.home_page.home_link_button.clicked.connect(self.home_page.parent_link)

        # Download Page
        # ///////////////////////////////////////////////////////////////
        self.download_page = PyDownloadPage(self.ui)
        logger.info('loading download page')
        self.ui.load_pages.download_page_all_config.addWidget(self.download_page)

        def download_status (download_):
            logger.info(download_)
            row = download_[0]
            col = 4
            text = 'Reload' if '-1' == download_[2] else download_[2]
            bg_color = '#037AFF' if text == 'Downloading' else '#495A71'
            if self.child_widget.video_select_table.cellWidget(row, col):
                self.child_widget.video_select_table.cellWidget(row, col).download_button.setText(text)
                self.child_widget.video_select_table.cellWidget(row, col).download_button.setEnabled(False)
                self.child_widget.video_select_table.cellWidget(row, col).download_button.setStyleSheet(
                        f'''border: none; padding-left: 10px; padding-right: 5px; border-radius: 8;
                            background-color: {bg_color};''')

        # Download status
        self.download_page.download_page_status_.connect(download_status)

        # Setting Page
        # ///////////////////////////////////////////////////////////////
        self.settings_page = PySettingsPage(self.ui)
        logger.info('loading settings page')
        self.ui.load_pages.setting_page_all_config.addWidget(self.settings_page)

        # ///////////////////////////////////////////////////////////////
        # END - EXAMPLE CUSTOM WIDGETS
        # ///////////////////////////////////////////////////////////////

    # RESIZE GRIPS AND CHANGE POSITION
    # Resize or change position when window is resized
    # ///////////////////////////////////////////////////////////////
    def resize_grips (self):
        if self.settings["custom_title_bar"]:
            self.left_grip.setGeometry(5, 10, 10, self.height())
            self.right_grip.setGeometry(self.width() - 15, 10, 10, self.height())
            self.top_grip.setGeometry(5, 5, self.width() - 10, 10)
            self.bottom_grip.setGeometry(5, self.height() - 15, self.width() - 10, 10)
            self.top_right_grip.setGeometry(self.width() - 20, 5, 15, 15)
            self.bottom_left_grip.setGeometry(5, self.height() - 20, 15, 15)
            self.bottom_right_grip.setGeometry(self.width() - 20, self.height() - 20, 15, 15)
