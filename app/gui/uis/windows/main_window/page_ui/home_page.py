from PySide6.QtCore import QPoint, Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QHBoxLayout, QHeaderView, QTableWidgetItem,
                               QVBoxLayout, QWidget)

from app.gui.core.json_themes import Themes
from app.gui.downloader.api.gui_call_interface import run
from app.gui.downloader.log import logger
from app.gui.downloader.setting.database_action import select_record
from app.gui.downloader.setting.database_action.insert_record import \
    insert_single_line
from app.gui.downloader.utils import byte_to_mb
from app.gui.uis.tools.utils import (max_h_w, min_h_w, run_in_thread_pool,
                                     table_sort_display)
from app.gui.widgets.py_lable.py_lable import PyLabel
from app.gui.widgets.py_line_edit.py_line_edit import PyLineEdit
from app.gui.widgets.py_message.py_message import PyMessageBox
from app.gui.widgets.py_push_button.py_push_button import PyPushButton
from app.gui.widgets.py_table_widget.py_table_widget import PyTableWidget


class ButtonLayout(QWidget):
    def __init__(self):
        super().__init__()
        self.download_button = PyPushButton(
            "Download", 8, "#9EA5AF", "#4A5A71", "#4A5A71", "#037aff"
        )
        hb_button = QHBoxLayout()
        hb_button.addWidget(self.download_button)
        hb_button.setAlignment(Qt.AlignCenter)
        hb_button.setContentsMargins(0, 0, 0, 0)
        # max_h_w(self.download_button, 48, 180)
        self.download_button.setFixedSize(180, 48)
        self.setLayout(hb_button)


class PyLinkParse(QWidget):
    download_action = Signal(list, list, list, list)
    download_data_button_action = Signal(list)

    def __init__(self, ui, result, parent=None):
        self.ui = ui
        self.download_num = []
        self.chebox_status = []
        # LOAD THEME COLOR
        # ///////////////////////////////////////////////////////////////
        themes = Themes()
        self.themes = themes.items
        super(PyLinkParse, self).__init__(parent)
        self.formats = ""
        self.insert_id = ""
        self.child_row_1 = QVBoxLayout()

        self.child_row_2 = QVBoxLayout()

        if result:
            self.url_id = result["url_id"]
            self.webpage_url = result["webpage_url"]
            self.result = [
                {
                    "title": result["title"],
                    "duration": result["duration"],
                    "url_id": result.get("url_id"),
                }
            ]
            self.title = result["title"].replace("'", "")
            self.uploader = result["uploader"]
            self.duration = result["duration"]
            self.cove = result["cove"] if result["cove"] else ""
            self.cove_height = result["height"] if result["height"] else ""
            self.cove_width = result["width"] if result["width"] else ""
            self.formats = result["formats"]

            # LOAD COVE
            self.link_basic_information = QHBoxLayout()

            if self.cove:
                pixmap = QPixmap(self.cove)
                # self.display_cove = PyLabel(pixmap=pixmap)
                self.display_cove = PyLabel()
                self.display_cove.setPixmap(pixmap)
                self.display_cove.resize(pixmap.width(), pixmap.height())
                max_h_w(self.display_cove, 150, 180)
                # self.display_cove.setScaledContents(True)
            else:
                self.display_cove = PyLabel("暂无")

            # LOAD LINK BASIC INFO
            self.link_basic_info = QVBoxLayout()
            self.link_basic_title = QHBoxLayout()
            self.link_basic_uploader = QHBoxLayout()
            self.link_basic_duration = QVBoxLayout()

            # LOAD INFO
            self.link_title = PyLabel(f"Title:    {self.title}")
            self.link_uploader = PyLabel(f"Uploader:    {self.uploader}")
            self.link_duration = PyLabel(f"Duration:    {self.duration}")
            # ADD WIDGET
            self.link_basic_title.addWidget(self.link_title)
            self.link_basic_uploader.addWidget(self.link_uploader)
            # margin
            self.link_basic_uploader.addSpacing(24)
            self.link_basic_uploader.addWidget(self.link_duration)
            self.link_basic_uploader.addSpacing(24)
            # max_h_w(self.download_data_button, 48, 100)
            # self.link_basic_uploader.addWidget(self.download_data_button)

            self.link_basic_info.addLayout(self.link_basic_title)
            self.link_basic_info.addLayout(self.link_basic_uploader)
            self.link_basic_info.addLayout(self.link_basic_info)

            self.formats = table_sort_display(self.formats)

            self.link_basic_information.addWidget(self.display_cove)
            self.link_basic_information.addLayout(self.link_basic_info)
            self.child_row_1.addLayout(self.link_basic_information)

        self.video_select_table = PyTableWidget(is_action=True)
        self.video_select_table.setColumnCount(5)

        # Columns / Header
        self.column_1 = QTableWidgetItem()
        self.column_1.setTextAlignment(Qt.AlignCenter)
        self.column_1.setText("Num")

        self.column_2 = QTableWidgetItem()
        self.column_2.setTextAlignment(Qt.AlignCenter)
        self.column_2.setText("Quality")

        self.column_3 = QTableWidgetItem()
        self.column_3.setTextAlignment(Qt.AlignCenter)
        self.column_3.setText("FileType")

        self.column_4 = QTableWidgetItem()
        self.column_4.setTextAlignment(Qt.AlignCenter)
        self.column_4.setText("FileSize")

        self.column_5 = QTableWidgetItem()
        self.column_5.setTextAlignment(Qt.AlignCenter)
        self.column_5.setText("Download")

        # Set column
        self.video_select_table.setHorizontalHeaderItem(0, self.column_1)
        self.video_select_table.setHorizontalHeaderItem(1, self.column_2)
        self.video_select_table.setHorizontalHeaderItem(2, self.column_3)
        self.video_select_table.setHorizontalHeaderItem(3, self.column_4)
        self.video_select_table.setHorizontalHeaderItem(4, self.column_5)

        def table_data_handle(table_cell):
            self.pass_text = QTableWidgetItem(table_cell)
            self.pass_text.setFlags(Qt.ItemIsEnabled)
            self.pass_text.setTextAlignment(Qt.AlignCenter)
            return self.pass_text

        if self.formats:
            for format_list in self.formats:
                filessize = byte_to_mb(format_list["filesize"])
                row_number = self.video_select_table.rowCount()
                self.video_select_table.insertRow(row_number)  # Insert row
                chk_box_item = QTableWidgetItem()
                # chk_box_item.setText(format_list['format_note'])
                chk_box_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                chk_box_item.setCheckState(Qt.Unchecked)
                button_ = ButtonLayout()
                button_.download_button.clicked.connect(self.single_button_clicked)
                self.video_select_table.setItem(
                    row_number, 0, table_data_handle(f"{row_number + 1}")
                )
                self.video_select_table.setItem(
                    row_number, 1, table_data_handle(format_list["format_note"])
                )
                self.video_select_table.setItem(
                    row_number, 2, table_data_handle(format_list["ext"])
                )
                self.video_select_table.setItem(
                    row_number, 3, table_data_handle(filessize)
                )
                # self.video_select_table.setCellWidget(row_number, 4, download_button)
                self.video_select_table.setCellWidget(row_number, 4, button_)
                self.video_select_table.setRowHeight(row_number, 50)
            # self.video_select_table.item(0, 1).setData()

        # config table style
        self.video_select_table.setShowGrid(False)
        self.video_select_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        # self.video_select_table.setAlternatingRowColors(True)
        self.video_select_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.Interactive
        )
        self.video_select_table.horizontalHeader().setSectionResizeMode(
            4, QHeaderView.Interactive
        )
        self.video_select_table.setAutoScroll(False)
        # self.video_select_table.setAlternatingRowColors(True)
        # self.video_select_table.setPalette(QPalette("#22272E"))
        # self.video_select_table.setCornerButtonEnabled(False)
        self.video_select_table.setColumnWidth(0, 80)
        self.video_select_table.setColumnWidth(4, 200)

        self.video_select_table.itemEntered.connect(
            lambda item: self.video_select_table.handleItemEntered(item)
        )
        self.video_select_table.itemExited.connect(
            lambda item: self.video_select_table.handleItemExited(item)
        )

        # GET TABLE CHE  BOX CHECK

        def on_tableWidget_itemChanged(row, column):
            logger.info(f"{row, column}")

        self.allQVBoxLayout = QVBoxLayout()
        if not result:
            self.video_select_table.setMaximumHeight(550)
            self.video_select_table.setMinimumHeight(500)

        self.child_row_2.addWidget(self.video_select_table)
        self.allQVBoxLayout.addLayout(self.child_row_1)
        self.allQVBoxLayout.addLayout(self.child_row_2)
        self.setLayout(self.allQVBoxLayout)

        # self.download_data_button_action.connect(self.display_download_button)

    # def display_download_button(self, dowm):
    #     print("打印内容", dowm)
    #     if self.download_num:
    #         # palette = QPalette()
    #         p = self.download_data_button.palette()
    #         p.setColor(QPalette.Button, Qt.red)
    #         self.download_data_button.setPalette(p)
    #         self.download_data_button.setAutoFillBackground(True)
    #         self.download_data_button.setFlat(True)
    #         # self.show()
    #         # palette.setColor(Background)
    #         # self.download_data_button.setStyleSheet("background-color:#037aff")
    #     pass

    def chebox_down_action(self, state, chebox_down):
        self.sender()
        # index = self.video_select_table.indexAt(chebox.pos())

    def ready_download_data(self):
        self.download_action.emit(
            self.result, self.download_num, self.formats, [self.insert_id]
        )
        for i in self.download_num:
            self.video_select_table.cellWidget(i, 4).setText("download in progress")
            self.video_select_table.cellWidget(i, 4).etEnabled(False)

    def single_button_clicked(self):
        button = self.sender()
        x = button.parentWidget().frameGeometry().x()
        y = button.parentWidget().frameGeometry().y()
        index = self.video_select_table.indexAt(QPoint(x, y))
        format_id = self.formats[index.row()].get("format_id")
        result = select_record(
            {"url_id": [self.url_id, "AND"], "format_id": int(format_id)}
        )
        logger.info(f"select record:{result}")
        if not result:
            self.video_select_table.cellWidget(
                index.row(), index.column()
            ).download_button.setText("Downloading")
            self.video_select_table.cellWidget(
                index.row(), index.column()
            ).download_button.setEnabled(False)
            self.video_select_table.cellWidget(
                index.row(), index.column()
            ).download_button.setStyleSheet(
                """
                    border: none;
                    padding-left: 10px;
                    padding-right: 5px;
                    border-radius: 8;
                    background-color: #037AFF;
                """
            )
            quality = self.formats[index.row()].get("format_note")
            file_type = self.formats[index.row()].get("ext")
            file_size = byte_to_mb(self.formats[index.row()].get("filesize"))
            insert_data = {
                "title": self.title,
                "uploader": self.uploader,
                "duration": self.duration,
                "quality": quality,
                "file_type": file_type,
                "file_size": file_size,
                "format_id": format_id,
                "url_id": self.url_id,
                "webpage_url": self.webpage_url,
            }
            self.insert_id = insert_single_line(insert_data)
            logger.info(f"插入——id{self.insert_id}")
            if index.isValid():
                logger.info(f"{[index.row()], [self.insert_id]}")
                self.download_action.emit(
                    self.result, [index.row()], self.formats, [self.insert_id]
                )
        else:
            if len(result) == 1:
                result = result[0]
                messagebox = PyMessageBox(text="Downloading")
                # messagebox.setWindowIcon(Functions.set_svg_icon("icon_warm_prompt.svg"))
                messagebox.setWindowTitle("Download Prompt")
                if result.get("download_status") == 1:
                    messagebox.setText("Downloading...")
                else:
                    messagebox.setText("Download already saved whether overwrite?")
                    messagebox.addButton("Cancel", messagebox.RejectRole)
                messagebox.addButton("Okay", messagebox.AcceptRole)
                #
                messagebox.exec()


class PyHomePage(QWidget):
    """定义一种信号，因为有文本框和进度条两个类，此处要一个参数，类型是：dict"""

    child_si = Signal(dict)

    def __init__(self, ui, parent=None):
        self.ui = ui
        self.child_exsit = 1
        super(PyHomePage, self).__init__(parent)
        self.home_row_1 = QHBoxLayout()
        self.home_row_2 = QHBoxLayout()
        self.home_link_and_button = QHBoxLayout()
        self.home_link_input = PyLineEdit(
            place_holder_text="input link",
        )

        self.home_link_button = PyPushButton(
            "Download", 8, "#9EA5AF", "#4A5A71", "#4A5A71", "#037aff"
        )
        max_h_w(self.home_link_input, 48, 700)
        max_h_w(self.home_link_button, 48, 180)
        min_h_w(self.home_link_input, 48, 680)
        min_h_w(self.home_link_button, 48, 180)
        self.home_link_and_button.addWidget(self.home_link_input, 1)
        self.home_link_and_button.addSpacing(46)
        self.home_link_and_button.addWidget(self.home_link_button, 1)
        self.home_row_1.addLayout(self.home_link_and_button)

        self.homeQHBoxLayout = QVBoxLayout()
        self.homeQHBoxLayout.addLayout(self.home_row_1, 0)
        self.homeQHBoxLayout.setSpacing(24)
        self.homeQHBoxLayout.addLayout(self.home_row_2, 0)
        logger.info("Home page init")
        self.setLayout(self.homeQHBoxLayout)

    def add_video_table(self, widget):
        self.home_row_2.addWidget(widget)

    def parent_link(self):
        # task = ThreadPoolExecutor(max_workers=2)
        logger.info("submit task")
        self.child_window_and_link_parem()

    @run_in_thread_pool()
    def child_window_and_link_parem(self):
        logger.info("get link")
        # 调用 emit方法发信号时，传入参数必须是这里指定的参数类型
        link = self.home_link_input.text()
        if link:
            logger.info("start perform task")
            result = run(link)
            self.child_si.emit(result)
