global_qss = """

* {
    font-family: "Poppins", 'Segoe UI', Arial, sans-serif;
}

QMainWindow, QDialog {
    background-color: #ffffff;
}


QTextEdit, QPlainTextEdit {
    border: 1px solid #ced4da;
    border-radius: 6px;
    padding: 12px;
    background-color: #fff;
    color: #212529;
    font-size: 10pt;
}

QTextEdit:focus, QPlainTextEdit:focus {
    border-color: #80bdff;
    outline: 0;
}

QPushButton {
    background-color: #f8f9fa;
    color: #007bff;
    border: 1px solid #dee2e6;
    border-radius: 5px;
    padding: 5px 10px;
    font-size: 9pt;
    margin: 2px;
    min-height: 28px;
}

QPushButton:hover {
    background-color: #e9ecef;
    border-color: #ced4da;
}

QPushButton:pressed {
    background-color: #dee2e6;
}

QPushButton:disabled {
    background-color: #e9ecef;
    color: #adb5bd;
    border-color: #dee2e6;
}

QTreeWidget {
    border: 1px solid #ced4da;
    border-radius: 6px;
    padding: 5px;
    background-color: #ffffff;
}
QTreeWidget::item {
    padding: 6px;
    height: 30px;
    border-radius: 3px;
    border-bottom: 1px solid #f2f2f2;
}
QTreeWidget::item:hover {
    background-color: #f0f0f0;
}
QTreeWidget::item:selected {
    background-color: #e7f0fd;
    color: #007bff;
}
QTreeWidget::item:hover:!selected {
    background-color: #f8f9fa;
}

QHeaderView::section {
    background-color: #f8f9fa;
    padding: 8px;
    border: none;
    border-right: 1px solid #ced4da;
    border-bottom: 1px solid #ced4da;
    font-weight: bold;
    color: #495057;
}
QHeaderView::section:checked {
    background-color: #007bff;
    color: white;
}

QScrollBar:vertical {
    background: #f0f0f0;
    width: 12px;
    margin: 0px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background: #c0c0c0;
    min-height: 20px;
    border-radius: 5px;
    margin: 2px;
}

QScrollBar::handle:vertical:hover {
    background: #a0a0a0;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: none;
}

QScrollBar:horizontal {
    background: #f0f0f0;
    height: 12px;
    margin: 0px;
    border-radius: 6px;
}

QScrollBar::handle:horizontal {
    background: #c0c0c0;
    min-width: 20px;
    border-radius: 5px;
    margin: 2px;
}

QScrollBar::handle:horizontal:hover {
    background: #a0a0a0;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0px;
}

QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {
    background: none;
}

QToolBar {
    background-color: #f8f9fa;
    border-bottom: 1px solid #dee2e6;
    spacing: 10px;
    padding: 5px 8px;
}

QFrame { 
    background-color: #f8f9fa; 
    border-radius: 8px; 
    border: 1px solid #ced4da;
}

QFrame[frameShape="4"], QFrame[frameShape="5"] {
    color: #dee2e6;
}

QLabel {
    font-weight: bold;
    color: #495057;
    margin-top: 5px;
    margin-bottom: 5px;
    border: none;
}

QLineEdit, QComboBox, QSpinBox {
    padding: 5px 8px;
    border: 1px solid #ced4da;
    border-radius: 4px;
    background-color: white;
    color: #212529;
    min-height: 25px;
    max-height: 25px;
}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
    border: 1px solid #80bdff;
}

QSpinBox::up-button, QSpinBox::down-button {
    width: 16px;
    border-radius: 2px;
}

QStatusBar {
    background-color: #f8f8f8;
    color: #505050;
    border-top: 1px solid #e0e0e0;
}

QProgressBar {
    border: 1px solid #ced4da;
    border-radius: 4px;
    background-color: #f8f9fa;
    text-align: center;
    height: 20px;
    min-height: 20px;
    max-height: 20px;
    padding: 0px;
    font-size: 9pt;
}
QProgressBar::chunk {
    background-color: #007bff;
    border-radius: 3px;
    width: 5px;
    margin: 0px;
}

QTabWidget::pane {
    border: 1px solid #dee2e6;
    border-radius: 5px;
    background-color: white;
}

QTabBar::tab {
    background-color: #f0f0f0;
    color: #495057;
    min-width: 90px;
    min-height: 25px;
    padding: 5px 12px;
    margin-right: 2px;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    border: 1px solid #dee2e6;
    border-bottom: none;
}

QTabBar::tab:selected {
    background-color: white;
    color: #007bff;
    font-weight: bold;
    border-bottom: 3px solid #007bff;
}

QTabBar::tab:hover:!selected {
    background-color: #e5e5e5;
}

QToolTip {
    border: 1px solid #e0e0e0;
    background-color: #f8f8f8;
    color: #404040;
    padding: 3px;
    border-radius: 4px;
}

QMenu {
    background-color: white;
    border: 1px solid #d0d0d0;
    border-radius: 4px;
    padding: 5px;
}

QMenu::item {
    padding: 5px 25px 5px 25px;
    border-radius: 3px;
}

QMenu::item:selected {
    background-color: #007bff;
    color: white;
}

QMenu::separator {
    height: 1px;
    background: #e0e0e0;
    margin: 5px 0px 5px 0px;
}

"""