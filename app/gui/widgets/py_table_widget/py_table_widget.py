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

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from PySide6.QtCore import QEvent, QModelIndex, QPersistentModelIndex, Signal
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView

# IMPORT STYLE
# ///////////////////////////////////////////////////////////////
from app.gui.widgets.py_table_widget.style import style

# PY PUSH BUTTON
# ///////////////////////////////////////////////////////////////


class PyTableWidget(QTableWidget):
    cellExited = Signal(int, int)
    itemExited = Signal(QTableWidgetItem)

    def __init__(
        self,
        radius=8,
        color="#FFF",
        # bg_color="#1B1E23",
        bg_color="#2D333B",
        selection_color="#22272E",
        header_horizontal_color="#22262C",
        header_vertical_color="#22262C",
        bottom_line_color="#555",
        grid_line_color="#555",
        scroll_bar_bg_color="#FFF",
        scroll_bar_btn_color="#333",
        context_color="#00ABE8",
        is_action=False,
        # last_row='',
    ):
        super().__init__()

        # PARAMETERS
        if is_action:
            self._last_index = QPersistentModelIndex()
            self.viewport().installEventFilter(self)
            self.setMouseTracking(True)
            self.setShowGrid(False)
            self.setFocusPolicy(Qt.NoFocus)
            self.setSelectionMode(QAbstractItemView.ContiguousSelection)
            self.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.setCornerButtonEnabled(False)
            self.verticalHeader().setVisible(False)
            self.setMouseTracking(True)
        self.current_row = -1
        # self.last_row = last_row

        # self.cellEntered.connect(lambda row, cloum: self.entered_cell(row))

        # SET STYLESHEET
        self.set_stylesheet(
            radius,
            color,
            bg_color,
            header_horizontal_color,
            header_vertical_color,
            selection_color,
            bottom_line_color,
            grid_line_color,
            scroll_bar_bg_color,
            scroll_bar_btn_color,
            context_color,
        )

    # SET STYLESHEET
    def set_stylesheet(
        self,
        radius,
        color,
        bg_color,
        header_horizontal_color,
        header_vertical_color,
        selection_color,
        bottom_line_color,
        grid_line_color,
        scroll_bar_bg_color,
        scroll_bar_btn_color,
        context_color,
    ):
        # APPLY STYLESHEET
        style_format = style.format(
            _radius=radius,
            _color=color,
            _bg_color=bg_color,
            _header_horizontal_color=header_horizontal_color,
            _header_vertical_color=header_vertical_color,
            _selection_color=selection_color,
            _bottom_line_color=bottom_line_color,
            _grid_line_color=grid_line_color,
            _scroll_bar_bg_color=scroll_bar_bg_color,
            _scroll_bar_btn_color=scroll_bar_btn_color,
            _context_color=context_color,
        )
        self.setStyleSheet(style_format)
        return style_format

    # def mouseMoveEvent(self, event):
    #     row = self.indexAt(event.pos()).row()
    #     print(row)
    #     self.updateRow(row)
    #
    # def leaveEvent(self, event):
    #     print("离开")
    #     self.setHoverRow(-1)
    #
    # def updateRow(self, row):
    #     if row == self.current_row:
    #         return
    #
    # def setHoverRow(self, hover_row):
    #     self.hover_row = hover_row
    # def entered_cell(self, row):
    #     print(row)
    #     for i in range(1, 4):
    #         self.item(row, i).setBackground(QColor("#262A31"))

    def eventFilter(self, widget, event):
        if widget is self.viewport():
            index = self._last_index
            if event.type() == QEvent.MouseMove:
                index = self.indexAt(event.pos())
            elif event.type() == QEvent.Leave:
                index = QModelIndex()
            if index != self._last_index:
                row = self._last_index.row()
                column = self._last_index.column()
                item = self.item(row, column)
                if item is not None:
                    self.itemExited.emit(item)
                self.cellExited.emit(row, column)
                self._last_index = QPersistentModelIndex(index)
        return QTableWidget.eventFilter(self, widget, event)

    # def is_entered(self, item, is_entered):
    #     if is_entered:
    #         self.handleItemEntered(item)
    #     else:
    #         self.handleItemExited(item)

    def handleItemEntered(self, item):
        pass

    def handleItemExited(self, item):
        pass
