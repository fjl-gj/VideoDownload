import sys
import os

from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFileDialog

from app.gui.downloader.setting.database_action import select_record
from app.gui.downloader.setting.global_var_ import globals_var
from app.gui.core.functions import Functions
from app.gui.uis.tools.utils import max_h_w, default_thread_index
from app.gui.downloader.utils import check_proxy
from app.gui.widgets import *


class PySettingsPage(QWidget):
    def __init__(self, ui, parent=None):
        self.ui = ui
        self.threads = ["1", "2", "4"]
        self.themes = ["default", "bright_theme", "dracula"]
        self.language = ["English"]
        self.setting_down_path = globals_var.DOWNLOAD_DIRECTORY
        self.setting_thread = globals_var.THREAD
        self.setting_language = globals_var.LANGUAGE
        self.setting_theme = globals_var.THEME
        self.setting_proxy_http = globals_var.setting_proxy_http
        super(PySettingsPage, self).__init__(parent)

        self.setting_row_1 = QHBoxLayout()
        self.setting_row_2 = QHBoxLayout()
        self.setting_row_3 = QHBoxLayout()
        self.setting_row_4 = QHBoxLayout()
        self.setting_row_5 = QHBoxLayout()
        self.setting_row_save = QHBoxLayout()

        self.setting_language_select = QHBoxLayout()
        self.setting_page_language_lable = PyLabel('Language')
        self.setting_page_select_language = PyComboBox(self.language)
        language_index = default_thread_index(globals_var.LANGUAGE, self.language)
        self.setting_page_select_language.setCurrentIndex(language_index)

        max_h_w(self.setting_page_language_lable, 48, 80)
        max_h_w(self.setting_page_select_language, 48, 570)

        self.setting_language_select.addWidget(self.setting_page_language_lable)
        self.setting_language_select.addWidget(self.setting_page_select_language)
        self.setting_row_1.addLayout(self.setting_language_select)

        self.setting_download_location = QHBoxLayout()
        self.setting_page_directory_lable = PyLabel('Path')
        self.setting_page_display_directory = PyLineEdit(self.setting_down_path)
        self.setting_page_select_directory = PyIconButton(
            icon_path=Functions.set_svg_icon("icon_folder_open.svg"),
            parent=self,
            app_parent=self.ui.central_widget,
            tooltip_text="alter directory",
        )
        max_h_w(self.setting_page_directory_lable, 48, 80)
        max_h_w(self.setting_page_display_directory, 48, 500)
        max_h_w(self.setting_page_select_directory, 48, 70)

        self.setting_download_location.addWidget(self.setting_page_directory_lable, 0)
        self.setting_download_location.addWidget(self.setting_page_display_directory, 1)
        self.setting_download_location.addWidget(self.setting_page_select_directory, 0)
        self.setting_row_2.addLayout(self.setting_download_location, 1)

        self.setting_thread_select = QHBoxLayout()
        self.setting_page_thread_label = PyLabel('Task')
        self.setting_page_thread_select = PyComboBox(self.threads)
        thread_index = default_thread_index(globals_var.THREAD, self.threads)
        self.setting_page_thread_select.setCurrentIndex(thread_index)
        max_h_w(self.setting_page_thread_label, 48, 80)
        max_h_w(self.setting_page_thread_select, 48, 570)
        self.setting_thread_select.addWidget(self.setting_page_thread_label)
        self.setting_thread_select.addWidget(self.setting_page_thread_select)
        self.setting_row_3.addLayout(self.setting_thread_select, 1)

        self.setting_themes_select = QHBoxLayout()
        self.setting_page_themes_lable = PyLabel('Themes')
        self.setting_page_select_themes = PyComboBox(self.themes)
        theme_index = default_thread_index(globals_var.THEME, self.themes)
        self.setting_page_select_themes.setCurrentIndex(theme_index)

        max_h_w(self.setting_page_themes_lable, 48, 80)
        max_h_w(self.setting_page_select_themes, 48, 570)
        self.setting_themes_select.addWidget(self.setting_page_themes_lable)
        self.setting_themes_select.addWidget(self.setting_page_select_themes)
        self.setting_row_4.addLayout(self.setting_themes_select)

        self.setting_proxy = QHBoxLayout()
        self.setting_page_proxy_label = PyLabel('PROXY')
        self.setting_page_proxy_input = PyLineEdit(text=self.setting_proxy_http,
                                                   place_holder_text='(http://xxx:xxxx) ; or '
                                                                     '(http://xxx:xxxx) ; (https://xxx:xxxx)')
        max_h_w(self.setting_page_proxy_label, 48, 80)
        max_h_w(self.setting_page_proxy_input, 48, 570)
        self.setting_proxy.addWidget(self.setting_page_proxy_label)
        self.setting_proxy.addWidget(self.setting_page_proxy_input)
        self.setting_row_5.addLayout(self.setting_proxy, 1)

        # save button

        self.setting_save_button = PyPushButton('Save', 8, "#1b1e23", "#4A5A71", "#4A5A71", "#037aff")
        max_h_w(self.setting_save_button, 48, 150)
        # self.setting_save_button = PyPushButton(
        #     # icon_path=Functions.set_svg_icon("icon_save_setting.svg"),
        #     parent=self,
        #     app_parent=self.ui.central_widget,
        #     tooltip_text="save setting",
        #     width=70,
        #     height=40,
        # )
        self.setting_row_save.addWidget(self.setting_save_button)

        self.settingQHBoxLayout = QVBoxLayout()
        self.settingQHBoxLayout.addLayout(self.setting_row_1, 1)
        self.settingQHBoxLayout.addLayout(self.setting_row_2, 1)
        self.settingQHBoxLayout.addLayout(self.setting_row_3, 1)
        self.settingQHBoxLayout.addLayout(self.setting_row_4, 1)
        self.settingQHBoxLayout.addLayout(self.setting_row_5, 1)
        self.settingQHBoxLayout.addLayout(self.setting_row_save, 0)

        self.setLayout(self.settingQHBoxLayout)

        def select_directory():
            '''
            select download directory (value invalid)
            :return: alter path (string)
            '''
            setting_file_path = QFileDialog.getExistingDirectory(dir=self.setting_down_path)
            self.setting_page_display_directory.setText(setting_file_path)
            return setting_file_path

        def select_thread():
            '''
            select download thread (value invalid)
            :return:
            '''
            setting_thread = self.setting_page_thread_select.currentText()

        def save_setting():
            '''
            save setting all config
            :return:
            '''
            self.setting_language = self.setting_page_select_language.currentText()
            self.setting_down_path = self.setting_page_display_directory.text()
            self.setting_thread = self.setting_page_thread_select.currentText()
            self.setting_theme = self.setting_page_select_themes.currentText()
            self.setting_proxys = self.setting_page_proxy_input.text()
            is_reboot = ''
            # old_theme = globals_var.THEME
            http_proxy = check_proxy(self.setting_proxys)
            if self.setting_theme != globals_var.THEME:
                is_reboot = True
            globals_var.LANGUAGE = self.setting_language
            globals_var.update_download_directory(self.setting_down_path)
            globals_var.update_threads(self.setting_thread)
            globals_var.update_themes(self.setting_theme)
            if http_proxy:
                globals_var.update_proxy(self.setting_proxys)
                globals_var.PROXY = http_proxy
            else:
                globals_var.update_proxy('None')
                globals_var.PROXY = 'None'
            if is_reboot:
                result = select_record({'download_status': 1})
                messagebox = PyMessageBox(text = "Settinging")
                messagebox.setWindowTitle("Update Setting")
                if result:
                    messagebox.setText("You are advised to pause or close the download and restart the application "
                                       "to take effect ！")
                    messagebox.addButton("OK", messagebox.RejectRole)
                    messagebox.exec()
                else:
                    messagebox.setText("Restart the application to take effect！")
                    messagebox.addButton("OK", messagebox.RejectRole)
                    messagebox.exec()

        # SELECT DIR EVENT
        self.setting_page_select_directory.clicked.connect(select_directory)
        # SELECT THREAD
        self.setting_page_thread_select.currentIndexChanged.connect(select_thread)
        # SETTING PROXY
        # ......

        self.setting_save_button.clicked.connect(save_setting)

    # def reboot(self):
    #     env = QProcessEnvironment.systemEnvironment()
    #     for name in os.environ:
    #         env.insert(f'{name}', os.environ[name])
    #     # qputenv("PATH", path)
    #     program = QApplication.applicationFilePath()
    #     arguments = QApplication.arguments()
    #     workingDirectory = QDir.currentPath()
    #     print(program, arguments, workingDirectory)
    #     process = QProcess()
    #     process.setProcessEnvironment(env)
    #     # process.setProcessEnvironment(sys.path)
    #     print(process.environment())
    #     process.startDetached(program, arguments, workingDirectory)
    #
    #     QApplication.exit()





