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
from PySide6.QtWidgets import QListWidget

# STYLE
# ///////////////////////////////////////////////////////////////
style = """
QListWidget {{
    background-color: {_bg_color};
    border-radius: {_radius}px;
    padding-left: 10px;
    padding-right: 10px;
    color: {_color};
}}
"""


# PY PUSH BUTTON
# ///////////////////////////////////////////////////////////////
class PyListWidget(QListWidget):
    def __init__(
        self,
        radius=8,
        border_size=2,
        color="#FFF",
        bg_color="#333",
        context_color="#00ABE8",
    ):
        super().__init__()

        # SET STYLESHEET
        self.set_stylesheet(
            radius,
            border_size,
            color,
            bg_color,
        )

    # SET STYLESHEET
    def set_stylesheet(
        self,
        radius,
        border_size,
        color,
        bg_color,
    ):
        # APPLY STYLESHEET
        style_format = style.format(
            _radius=radius,
            _border_size=border_size,
            _color=color,
            _bg_color=bg_color,
        )
        self.setStyleSheet(style_format)
