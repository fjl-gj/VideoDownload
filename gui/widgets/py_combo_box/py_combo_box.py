# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from PySide6.QtWidgets import QComboBox

# STYLE
# ///////////////////////////////////////////////////////////////
style = '''
    QComboBox {{
        background-color: {_bg_color};
        border-radius: {_radius}px;
        border: {_border_size}px solid transparent;
        padding-left: 10px;
        padding-right: 10px;
        selection-color: {_selection_color};
        selection-background-color: {_context_color};
        color: {_color};
    }}
    
    QComboBox QAbstractItemView {{
    outline: 0px solid gray;
    border: {_border_size}px solid transparent;
    color: {_color};
    background-color: {_bg_color};
    selection-background-color: {_context_color};
    }}
    
    QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 15px;

    border-left-width: 1px;
    border-left-color: darkgray;
    border-left-style: solid;
    border-top-right-radius: 3px;
    border-bottom-right-radius: 3px;
    }}
        
    QComboBox:focus {{
        border: {_border_size}px solid {_context_color};
        background-color: {_bg_color_active};
    }}
'''


class PyComboBox(QComboBox):
    def __init__(
        self,
        values,
        place_holder_text="",
        radius=8,
        border_size=2,
        color="#FFF",
        selection_color="#FFF",
        bg_color="#323742",
        bg_color_active="#323742",
        context_color="#00ABE8"
    ):
        super(PyComboBox, self).__init__()

        if values:
            self.addItems(values)
        if place_holder_text:
            self.setPlaceholderText(place_holder_text)

        # SET STYLESHEET
        self.set_stylesheet(
            radius,
            border_size,
            color,
            selection_color,
            bg_color,
            bg_color_active,
            context_color
        )

    # SET STYLESHEET
    def set_stylesheet(
            self,
            radius,
            border_size,
            color,
            selection_color,
            bg_color,
            bg_color_active,
            context_color
    ):
        # APPLY STYLESHEET
        style_format = style.format(
            _radius=radius,
            _border_size=border_size,
            _color=color,
            _selection_color=selection_color,
            _bg_color=bg_color,
            _bg_color_active=bg_color_active,
            _context_color=context_color
        )
        self.setStyleSheet(style_format)


def set_stylesheet():
    radius = 8,
    border_size = 2,
    color = "#FFF",
    selection_color = "#FFF",
    bg_color = "#333",
    bg_color_active = "#222",
    context_color = "#00ABE8"
    # APPLY STYLESHEET
    style = '''
    QComboBox {{
        background-color: {_bg_color};
        border-radius: {_radius}px;
        border: {_border_size}px solid transparent;
        padding-left: 10px;
        padding-right: 10px;
        selection-color: {_selection_color};
        selection-background-color: {_context_color};
        color: {_color};
    }}
    
    QComboBox QAbstractItemView {{
    outline: 0px solid gray;
    border: {_border_size}px solid transparent;
    color: {_color};
    background-color: {_bg_color};
    selection-background-color: {_context_color};
    }}
    
    QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 15px;

    border-left-width: 1px;
    border-left-color: darkgray;
    border-left-style: solid;
    border-top-right-radius: 3px;
    border-bottom-right-radius: 3px;
    }}
    
    QComboBox:focus {{
        border: {_border_size}px solid {_context_color};
        background-color: {_bg_color_active};
    }}
    '''

    return style.format(
        _radius=radius,
        _border_size=border_size,
        _color=color,
        _selection_color=selection_color,
        _bg_color=bg_color,
        _bg_color_active=bg_color_active,
        _context_color=context_color
    )
