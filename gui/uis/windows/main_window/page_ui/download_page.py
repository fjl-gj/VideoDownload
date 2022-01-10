import os
from concurrent.futures.thread import ThreadPoolExecutor

import requests
from PySide6.QtCore import QFileSystemWatcher
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QDialog, QFormLayout, QHBoxLayout, QLabel, QListWidgetItem, QSizePolicy, QSpacerItem, \
    QVBoxLayout, \
    QWidget

from gui.core.functions import Functions
from gui.downloader.log.log import logger
from gui.downloader.setting.database_action import delete_single_line_record, select_record, update_single_line_record
from gui.downloader.setting.global_var_ import globals_var
from gui.downloader.utils import byte_to_mb
from gui.downloader.utils import result_proxy
from gui.uis.tools.utils import replace_other_char
from gui.widgets import PyCircularProgress, PyIconButton, PyLabel, PyListWidget, PyMessageBox, PyPushButton

Task = ThreadPoolExecutor(max_workers = int(globals_var.THREAD))


class MyDialog(QDialog):
    def __init__(self, title, message, parent=None):
        super(MyDialog, self).__init__(parent=parent)
        form = QFormLayout(self)
        form.addRow(PyLabel(message))
        self.setWindowFlags((self.windowFlags() & ~Qt.WindowCloseButtonHint))
        self.setWindowTitle(title)
        self.hb = QHBoxLayout()
        self.button1 = PyPushButton('No', 8, "#000000", "#70B4FD", "#4A5A71", "#037aff")
        self.button1.setObjectName('1')
        self.button2 = PyPushButton('Yes,And Delete Local File', 8, "#000000", "#70B4FD", "#4A5A71", "#037aff")
        self.button2.setObjectName('2')
        self.button3 = PyPushButton('Cancel', 8, "#000000", "#70B4FD", "#4A5A71", "#037aff")
        self.button3.setObjectName('3')
        self.hb.addWidget(self.button1)
        self.hb.addWidget(self.button2)
        self.hb.addWidget(self.button3)
        form.addRow(self.hb)
        self.setStyleSheet('''
        border: 1px;
        padding-left: 10px;
        padding-right: 10px;
        border-radius: 8;
        background-color: #FFFFFF;
        ''')


def set_id (sql_id):
    return sql_id


class PyDownloadWidget(QWidget):
    set_value = Signal(int)
    download_widget_status = Signal(list)

    def __init__ (self, ui, result, formats, sql_id, file_system_watcher, directories, i, parent = None):
        self.ui = ui
        self.init_down = 0
        self.download_stat = 0
        self.file_system_watcher = file_system_watcher
        self.directories = directories
        self.index = i
        self.values = formats.get('down_percentage') if formats.get('down_percentage') else 0
        self.pause_status = 0
        self.delete_status = 0
        self.resume_status = 0
        # self.id 精准数据库id
        self.id = sql_id
        self.sql_id = formats.get('id')
        self.title = result[0].get('title')
        self.duration = result[0].get('duration')
        self.url_id = result[0].get('url_id')
        self.file_size = byte_to_mb(formats.get('filesize'))
        self.file_type = formats.get('file_type') if formats.get('file_type') else formats.get('ext')
        self.file_note = formats.get('format_note')
        self.format_id = formats.get('format_id')
        self.format = formats.get('format')
        self.formats = formats
        self.size = formats.get('size') if formats.get('size') else formats.get('filesize')
        self.down_file_size = formats.get('down_file_size') if formats.get('down_file_size') else 0
        self.chunk_size = 1024
        self.file_name = 'VD' + self.format + replace_other_char(self.title) + self.format_id
        if self.formats.get('file_path_name'):
            self.file_path_name = self.formats.get('file_path_name')
        else:
            self.file_path_name = globals_var.DOWNDIRECTORY.replace('\\', '\\\\') + f'\\\\{self.file_name}.{self.file_type}'
        self.file_path_info_json = globals_var.DOWNDIRECTORY + f'\\{self.file_name}.info.json'
        path = self.file_path_name.split('\\')[:-1]
        add_path = '\\'.join(path)
        if add_path in self.directories:
            logger.info(self.file_system_watcher.directories())
        else:
            self.file_system_watcher.addPath(add_path)
        super(PyDownloadWidget, self).__init__(parent)
        self.all_download_content = QVBoxLayout()
        logger.info(f"返回结果: {result}")

        self.single_download_content = QHBoxLayout()
        # LOAD single show
        self.load_progress = QHBoxLayout()

        # LOAD COVE
        self.load_progress_bar = PyCircularProgress(
                value = self.values,
                progress_width = 4,
                progress_color = "#568af2",
                text_color = "#568af2",
                font_size = 14,
                bg_color = "#3c4454",
        )
        self.load_progress_bar.setFixedSize(50, 50)

        self.load_progress.addWidget(self.load_progress_bar)

        # LOAD NAME
        self.load_info_min = QHBoxLayout()
        self.load_info = QVBoxLayout()
        # LOAD INFO
        self.link_index = QLabel(f'index:{sql_id}')
        self.link_index.setVisible(False)
        self.link_title = QLabel(f'Title：{self.title}')
        self.link_status = QLabel('DOWNLOADING')
        self.link_duration = QLabel(f'Duration：{self.duration}')
        self.link_file_size = QLabel(f'Size：{self.file_size}')
        self.link_file_type = QLabel(f'Type：{self.file_type}')
        self.link_file_note = QLabel(f'Quality：{self.file_note}')
        self.file_not_exists = QLabel('Status:  file        exists')
        # self.file_hb = QHBoxLayout()
        # self.file_hb.addWidget(self.file_not_exists)
        # spacerItem = QSpacerItem(50, 10, QSizePolicy.Maximum, QSizePolicy.Fixed)
        # self.file_hb.addItem(spacerItem)

        # self.file_not_exists.setMaximumHeight()

        self.load_info_min.addWidget(self.link_status)
        self.load_info_min.addWidget(self.link_duration)
        self.load_info_min.addWidget(self.link_file_size)
        self.load_info_min.addWidget(self.link_file_type)
        self.load_info_min.addWidget(self.link_file_note)
        if os.path.exists(self.file_path_name):
            self.load_info_min.addWidget(self.file_not_exists)
        # self.load_info_min.addLayout(self.file_hb)

        self.load_info_min.addWidget(self.link_index)
        self.load_info.addWidget(self.link_title)
        self.load_info.addLayout(self.load_info_min)
        # self.download_data_button = PyIconButton(icon_path=Functions.set_svg_icon('icon_confirm.svg'))

        # LOAD DELETE PAUSE BUTTON
        self.load_button = QHBoxLayout()
        self.load_delete = PyIconButton(Functions.set_svg_icon("icon_delete.svg"))
        self.load_pause = PyIconButton(Functions.set_svg_icon("icon_pause.svg"))
        self.load_resume = PyIconButton(Functions.set_svg_icon("icon_downloading.svg"))
        self.load_open_folder = PyIconButton(Functions.set_svg_icon("icon_folder_open.svg"))

        self.load_button.addWidget(self.load_delete)
        self.load_button.addWidget(self.load_pause)

        self.single_download_content.addLayout(self.load_progress)
        self.single_download_content.addLayout(self.load_info)
        self.single_download_content.addLayout(self.load_button)
        self.all_download_content.addLayout(self.single_download_content)

        self.setLayout(self.all_download_content)
        self.load_pause.clicked.connect(self.pause_status_action)
        self.load_resume.clicked.connect(self.resume_status_action)
        self.load_open_folder.clicked.connect(self.open_folder)

        self.load_delete.clicked.connect(self.delete_status_action)
        # self.file_system_watcher.fileChanged.connect(lambda path: self.file_changed(path))
        self.file_system_watcher.directoryChanged.connect(self.directory_changed)
        self.update_download_data()

    def history_download_record(self):
        if os.path.exists(self.file_path_name):
            pass
        else:
            self.file_not_exists = QLabel('Status:  files does not exists')
        if self.values == 100:
            self.finished_status()
        else:
            self.init_down = 1
            self.resume_status = 0
            self.pause_status = 1
            self.load_pause.close()
            self.link_status.setText('PAUSE')
            if not os.path.exists(self.file_path_name):
                self.values = 0
                self.load_progress_bar.value = 0
            self.load_button.addWidget(self.load_resume)
            self.directory_changed()

    def directory_changed (self):
        if self.init_down:
            if not os.path.exists(self.file_path_name):
                print(self.pause_status)
                if self.pause_status or self.load_progress_bar.value == 100:
                    self.init_down = 0
                    # self.file_not_exists = QLabel('files does not exists')
                    self.file_not_exists.setText('Status:  files does not exists')
                    self.load_open_folder.close()
                    self.values = 0
                    self.load_progress_bar.value = 0
                    self.load_progress_bar.update()
                    self.pause_status_action()
                    self.load_info_min.addWidget(self.file_not_exists)

    def delete_status_action(self):
        self.link_index.setText("-1")
        self.message = MyDialog('DELETE', 'Deleting a Local File', self)
        # print("进入")
        self.message.button1.clicked.connect(self.file_handling)
        self.message.button2.clicked.connect(self.file_handling)
        self.message.button3.clicked.connect(self.file_handling)
        self.message.exec()

    def file_handling(self):
        btn = self.sender()
        x = btn.objectName()
        print(x, type(x))
        if x == '2':
            delete_single_line_record({'id': self.id})
            if os.path.exists(self.file_path_name):
                os.remove(self.file_path_name)
            if self.index:
                self.download_widget_status.emit([self.index, self.format_id, '-1'])
        elif x == '1':
            delete_single_line_record({'id': self.id})
            self.download_widget_status.emit([self.index, self.format_id, '-1'])
        self.message.close()

    def pause_status_action (self):
        """
        pause status
        history download ： 根据百分比配置数据
        :return:
        """
        # if self.values == 100:
        #     self.finished_status()
        # else:
        if not self.pause_status:
            self.init_down = 0
            self.pause_status = 1
            self.resume_status = 0
            self.load_pause.close()
            self.link_status.setText('PAUSE')
            self.load_resume = PyIconButton(Functions.set_svg_icon("icon_downloading.svg"))
            self.load_button.addWidget(self.load_resume)
            self.load_resume.clicked.connect(self.resume_status_action)
            if self.index:
                self.download_widget_status.emit([self.index, self.format_id, 'PAUSE'])
            # if self.down_file_size:
            #     if os.path.exists(self.file_path_name):
            #         pass
            #     else:

    def resume_status_action (self):
        if self.values != 100 and self.values < 100:
            if not self.resume_status:
                self.init_down = 0
                self.pause_status = 0
                self.resume_status = 1
                self.load_resume.close()
                self.link_status.setText('RESUME-DOWNLOAD')
                self.load_pause = PyIconButton(Functions.set_svg_icon("icon_pause.svg"))
                self.load_button.addWidget(self.load_pause)
                self.load_pause.clicked.connect(self.pause_status_action)
                Task.submit(self.download_data)
                # Task.submit(self.youtube_dl_download)
                if self.index:
                    self.download_widget_status.emit([self.index, self.format_id, 'RESUME-DOWNLOAD'])

    def finished_status (self):
        """
        finished download
        :return:
        """
        # if self.load_progress_bar.value == 100:
        self.init_down = 1
        self.pause_status = 0
        self.resume_status = 0
        self.load_pause.close()
        self.load_resume.close()
        self.link_status.setText('FINISHED')
        # if os.path.exists(self.file_path_name):
        if os.path.exists(self.file_path_name):
            self.load_button.addWidget(self.load_open_folder)
        else:
            self.values = 0
            self.load_progress_bar.value = 0
            self.down_file_size = 0
            self.load_resume = PyIconButton(Functions.set_svg_icon("icon_downloading.svg"))
            self.load_resume.clicked.connect(self.resume_status_action)
            self.load_button.addWidget(self.load_resume)
            # self.load_button.addWidget(self.load_open_folder)

    def open_folder (self):
        if os.path.exists(self.file_path_name):
            file = os.path.realpath(self.file_path_name)
            os.system(f'explorer /select, {file}')
        else:
            os.startfile(globals_var.DOWNDIRECTORY)

    def update_progress (self, value):
        query_all = {'id': self.id}
        update_all = {'down_percentage': value, 'down_file_size': self.down_file_size}
        update_single_line_record(query_all, update_all)

    def update_download_data (self):
        query_all = {'id': self.id}
        if self.formats.get('url'):
            update_all = {'down_url': self.formats.get('url'), 'down_file_size': 0, 'size': self.size,
                          'file_path_name': self.file_path_name}
            update_single_line_record(query_all, update_all)

    # def hook_progress(self, d):
    #     print(d.get("_percent_str"), d.get("_eta_str"), d.get("_speed_str"))
    #     self.load_progress_bar.value = float(_percent_str)
    #
    # def youtube_dl_download(self):
    #     ydl_opts = {
    #         # 'proxy': 'https://127.0.0.1:1087',
    #         # 'format': f'{self.format_id}/best',
    #         'store_true': True,
    #         'writeinfojson': True,
    #         'load_info_filename':  self.file_path_info_json,
    #         'progress_hooks': [self.hook_progress],
    #         'outtmpl': self.file_path_name,
    #     }
    #     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #         ydl.download([self.formats['url']])

    def download_data (self):
        self.init_down = 0
        self.file_not_exists.setText('')
        # _proxies = {"https": "http://127.0.0.1:1087", "http": "http://127.0.0.1:1087"}
        _proxies = result_proxy(globals_var.PROXY)
        logger.info(_proxies)
        # _proxies = {"http": None, "https": None}
        if not os.path.exists(self.file_path_name):
            self.down_file_size = 0
        _headers = {
            'Range': f'bytes={self.down_file_size}-{self.size}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/92.0.4515.107 Safari/537.36',
        }
        url = self.formats.get('down_url') if self.formats.get('down_url') else self.formats.get('url')
        # logger.info(f'{self.down_file_size}, {self.size}, {url}')

        resp = requests.get(url, headers = _headers, proxies = _proxies, stream = True, timeout=15)
        if 400 <= resp.status_code:
            message = PyMessageBox(text = "DOWNLOAD TASK")
            message.setWindowTitle("DELETE FILES")
            message.setText("Download link invalid\nPlease download again!!!")
            message.exec()
        # resp = requests.get(url, headers=_headers, stream=True, timeout=5)
        print(f'{self.down_file_size}, {self.size}, {url}, {self.file_path_name}')

        with open(self.file_path_name, 'ab') as file:
            logger.info("下载中")
            for data in resp.iter_content(chunk_size=self.chunk_size):
                if self.pause_status:
                    file.close()
                    break
                if self.delete_status:
                    file.close()
                    os.remove(self.file_path_name)
                    break
                file.write(data)
                self.down_file_size += len(data)
                value = int(self.down_file_size / self.size * 100)
                self.set_value.emit(value)

    def set_value_num (self, bar):
        if not self.download_stat:
            self.download_stat = 1
        if self.resume_status:
            if self.index:
                self.download_widget_status.emit([self.index, self.format_id, 'Downloading'])
            self.resume_status = 0
            self.link_status.setText('DOWNLOADING')
        self.load_progress_bar.value = bar
        self.load_progress_bar.update()
        self.update_progress(bar)
        if bar == 100:
            self.init_down = 1
            self.pause_status = 0
            self.resume_status = 0
            self.load_pause.close()
            self.load_resume.close()
            self.link_status.setText('FINISHED')
            # if os.path.exists(self.file_path_name):
            if os.path.exists(self.file_path_name):
                self.load_button.addWidget(self.load_open_folder)
                print("执行成功")
            else:
                self.values = 0
                self.load_progress_bar.value = 0
                self.load_resume = PyIconButton(Functions.set_svg_icon("icon_downloading.svg"))
                self.load_resume.clicked.connect(self.resume_status_action)
                self.load_button.addWidget(self.load_resume)
            if self.index:
                self.download_widget_status.emit([self.index, self.format_id, 'FINISHED'])
            # if os.path.exists(self.file_path_name):
                # self.load_button.addWidget(self.load_open_folder)


class PyDownloadPage(QWidget):
    download_page_status_ = Signal(list)

    def __init__ (self, ui, parent = None):
        self.ui = ui
        self.values = 1
        self.is_downloading = 1
        self.list_item = []
        super(PyDownloadPage, self).__init__(parent)
        self.file_system_watcher = QFileSystemWatcher()
        self.directories = [globals_var.DOWNDIRECTORY]
        self.file_system_watcher.addPaths(self.directories)
        self.download_page_all = QVBoxLayout()
        self.download_list = PyListWidget()
        self.all_download_content = QVBoxLayout()
        self.download_page_all.addWidget(self.download_list)
        self.setLayout(self.download_page_all)
        self.check_sql()

    def check_sql (self):
        results = select_record(False)
        if results:
            for result in results:
                sql_id = result.get('id')
                basics_info = [{'title': result.get('title'),
                                'duration': result.get('duration'),
                                'url_id': result.get('url_id')}]
                result['filesize'] = result.get('file_size')
                result['format_note'] = result.get('quality')
                result['format_id'] = str(result.get('format_id'))
                result['format'] = ''

                download_widget = PyDownloadWidget(self.ui, basics_info, result, sql_id, self.file_system_watcher,
                                                   self.directories, None)
                # download_widget.download_widget_status.connect(self.download_page_status_id)
                # sql_id = download_widget.set_id(sql_id)
                download_widget_item = QListWidgetItem(self.download_list)
                download_widget.set_value.connect(download_widget.set_value_num)
                download_widget_item.setSizeHint(download_widget.sizeHint())
                self.download_list.insertItem(0, download_widget_item)
                self.download_list.setSortingEnabled(True)
                self.download_list.sortItems(order = Qt.AscendingOrder)
                self.download_list.setItemWidget(download_widget_item, download_widget)

                # download_widget.load_progress_bar.value = 100
                download_widget.history_download_record()
                sqlid = download_widget.link_index

                download_widget.load_delete.clicked.connect(lambda: self.remove_list_item(self.download_list))
                self.list_item.insert(0, [download_widget, download_widget_item, sqlid])

    def add_download_item (self, result, download_num, formats, sql_id):
        for i in download_num:
            download_widget = PyDownloadWidget(self.ui, result, formats[i], sql_id[0], self.file_system_watcher,
                                               self.directories, i)
            download_widget.download_widget_status.connect(self.download_page_status_id)
            sql_id = set_id(sql_id)
            download_widget.set_value.connect(download_widget.set_value_num)
            download_widget_item = QListWidgetItem(self.download_list)
            download_widget_item.setSizeHint(download_widget.sizeHint())
            self.download_list.insertItem(0, download_widget_item)
            self.download_list.setSortingEnabled(True)
            self.download_list.sortItems(order = Qt.AscendingOrder)
            self.download_list.setItemWidget(download_widget_item, download_widget)
            # 这个任务核心上是异步且是 非阻塞的操作
            Task.submit(download_widget.download_data)
            # Task.submit(download_widget.youtube_dl_download)
            sqlid = download_widget.link_index
            self.list_item.insert(0, [download_widget, download_widget_item, sqlid])
            download_widget.load_delete.clicked.connect(lambda: self.remove_list_item(self.download_list, ))

    def remove_list_item (self, download_list):
        item_index = ''
        list_item_index = ''
        logger.info(self.list_item)
        for i in range(len(self.list_item)):
            if self.list_item[i][2].text() == "-1":
                list_item_index = i
                logger.info(self.list_item[i][0])
                item_index = self.download_list.row(self.list_item[i][1])
                logger.info(item_index)
        download_list.takeItem(item_index)
        del self.list_item[list_item_index]

    def download_page_status_id (self, download_status_id):
        self.download_page_status_.emit(download_status_id)
