from PySide6.QtWidgets import QMessageBox

# STYLE
# ///////////////////////////////////////////////////////////////
style = '''
QMessageBox {
    background-color: #F2F2F2; /* QMessageBox背景颜色 */
}

QMessageBox QLabel#qt_msgbox_label { /* textLabel */
    color: #298DFF;
    background-color: transparent;
    min-width: 240px; /* textLabel设置最小宽度可以相应的改变QMessageBox的最小宽度 */
    min-height: 40px; /* textLabel和iconLabel高度保持一致 */
}

QMessageBox QLabel#qt_msgboxex_icon_label { /* iconLabel */
    width: 40px;
    height: 40px; /* textLabel和iconLabel高度保持一致 */
}

QMessageBox QPushButton { /* QMessageBox中的QPushButton样式 */
    border: 1px solid #298DFF;
    border-radius: 3px;
    background-color: #F2F2F2;
    color: #298DFF;
    font-family: "Microsoft YaHei";
    font-size: 10pt;
    min-width: 70px;
    min-height: 25px;
}

QMessageBox QPushButton:hover {
    background-color: #298DFF;
    color: #F2F2F2;
}

QMessageBox QPushButton:pressed {
    background-color: #257FE6;
}

QMessageBox QDialogButtonBox#qt_msgbox_buttonbox { /* buttonBox */
    button-layout: 0; /* 设置QPushButton布局好像没啥作用 */
}

'''

# PY PUSH BUTTON
# ///////////////////////////////////////////////////////////////


class PyMessageBox(QMessageBox):
    def __init__(
            self,
            text,
            radius=8,
            border_size=2,
            color="#FFF",
            bg_color="#333",
            context_color="#00ABE8"
    ):
        super().__init__()

        # SET STYLESHEET
        self.setText(text)
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
        # style_format = style.format(
        #     _radius=radius,
        #     _border_size=border_size,
        #     _color=color,
        #     _bg_color=bg_color,
        # )
        # self.setStyleSheet(style_format)
        self.setStyleSheet(style)

