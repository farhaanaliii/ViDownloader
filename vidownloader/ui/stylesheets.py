global_qss = """
QWidget {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1e293b;
}

QMainWindow, QDialog, QMessageBox {
    background-color: #f8fafc;
}

QMessageBox QLabel {
    color: #1e293b;
    font-size: 9.5pt;
}

/* --- Input Fields --- */
QTextEdit, QPlainTextEdit {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 10px 12px;
    color: #1e293b;
    font-size: 9.5pt;
    selection-background-color: #dbeafe;
    selection-color: #1e40af;
}

QTextEdit:focus, QPlainTextEdit:focus {
    border: 1px solid #3b82f6;
}

QLineEdit, QComboBox, QSpinBox {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 4px 10px;
    color: #1e293b;
    font-size: 9.5pt;
    min-height: 26px;
    max-height: 26px;
}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
    border: 1px solid #3b82f6;
}

QLineEdit:disabled, QComboBox:disabled, QSpinBox:disabled {
    background-color: #f1f5f9;
    color: #94a3b8;
    border-color: #e2e8f0;
}

/* --- ComboBox & SpinBox Dropdowns --- */
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 24px;
    border-left: none;
    border-top-right-radius: 6px;
    border-bottom-right-radius: 6px;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 4px;
    selection-background-color: #eff6ff;
    selection-color: #2563eb;
    outline: none;
}

QSpinBox::up-button, QSpinBox::down-button {
    width: 18px;
    border: none;
    background: transparent;
}

QSpinBox::up-button:hover, QSpinBox::down-button:hover {
    background-color: #f1f5f9;
}

/* --- Buttons --- */
QPushButton {
    background-color: #ffffff;
    color: #334155;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 5px 14px;
    font-size: 9pt;
    font-weight: 500;
    min-height: 26px;
}

QPushButton:hover {
    background-color: #f8fafc;
    color: #0f172a;
    border-color: #94a3b8;
}

QPushButton:pressed {
    background-color: #f1f5f9;
    border-color: #64748b;
}

QPushButton:disabled {
    background-color: #f8fafc;
    color: #94a3b8;
    border-color: #e2e8f0;
}

QPushButton[primary="true"], QPushButton#primaryButton {
    background-color: #2563eb;
    color: #ffffff;
    border: 1px solid #2563eb;
    font-weight: 600;
}

QPushButton[primary="true"]:hover, QPushButton#primaryButton:hover {
    background-color: #1d4ed8;
    border-color: #1d4ed8;
}

QPushButton[primary="true"]:pressed, QPushButton#primaryButton:pressed {
    background-color: #1e40af;
    border-color: #1e40af;
}

QPushButton[primary="true"]:disabled, QPushButton#primaryButton:disabled {
    background-color: #93c5fd;
    color: #ffffff;
    border-color: #93c5fd;
}

QPushButton[success="true"], QPushButton#successButton {
    background-color: #ecfdf5;
    color: #059669;
    border: 1px solid #a7f3d0;
    font-weight: 500;
}

QPushButton[success="true"]:hover, QPushButton#successButton:hover {
    background-color: #d1fae5;
    color: #047857;
    border-color: #6ee7b7;
}

QPushButton[success="true"]:pressed, QPushButton#successButton:pressed {
    background-color: #a7f3d0;
    border-color: #34d399;
}

QPushButton[danger="true"], QPushButton#dangerButton {
    background-color: #fef2f2;
    color: #dc2626;
    border: 1px solid #fecaca;
    font-weight: 500;
}

QPushButton[danger="true"]:hover, QPushButton#dangerButton:hover {
    background-color: #fee2e2;
    color: #b91c1c;
    border-color: #fca5a5;
}

QPushButton[danger="true"]:pressed, QPushButton#dangerButton:pressed {
    background-color: #fecaca;
    border-color: #f87171;
}

QPushButton[danger="true"]:disabled, QPushButton#dangerButton:disabled {
    background-color: #f8fafc;
    color: #94a3b8;
    border-color: #e2e8f0;
}

/* --- Tree Widget (Data Table) --- */
QTreeWidget {
    background-color: #ffffff;
    alternate-background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 2px;
    outline: none;
}

QTreeWidget::item {
    padding: 6px 8px;
    min-height: 28px;
    border-bottom: 1px solid #f1f5f9;
    color: #1e293b;
}

QTreeWidget::item:hover:!selected {
    background-color: #f8fafc;
}

QTreeWidget::item:selected {
    background-color: #eff6ff;
    color: #1d4ed8;
}

QHeaderView::section {
    background-color: #f8fafc;
    color: #475569;
    padding: 8px 10px;
    font-weight: 600;
    font-size: 8.5pt;
    border: none;
    border-bottom: 1px solid #e2e8f0;
    border-right: 1px solid #f1f5f9;
}

QHeaderView::section:last {
    border-right: none;
}

/* --- Progress Bar --- */
QProgressBar {
    background-color: #f1f5f9;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    height: 20px;
    min-height: 20px;
    max-height: 20px;
    text-align: center;
    color: #1e293b;
    font-weight: 600;
    font-size: 8.5pt;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3b82f6, stop:1 #2563eb);
    border-radius: 7px;
}

/* --- Toolbar & Status Bar --- */
QToolBar {
    background-color: #ffffff;
    border-bottom: 1px solid #e2e8f0;
    spacing: 8px;
    padding: 6px 12px;
}

QStatusBar {
    background-color: #ffffff;
    border-top: 1px solid #e2e8f0;
    color: #64748b;
    font-size: 9pt;
}

/* --- Tabs --- */
QTabWidget::pane {
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    background-color: #ffffff;
    top: -1px;
}

QTabBar::tab {
    background-color: #f1f5f9;
    color: #64748b;
    padding: 8px 18px;
    margin-right: 4px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    border: 1px solid #e2e8f0;
    border-bottom: none;
    font-size: 9pt;
    font-weight: 500;
}

QTabBar::tab:selected {
    background-color: #ffffff;
    color: #2563eb;
    font-weight: 600;
    border-bottom: 2px solid #2563eb;
}

QTabBar::tab:hover:!selected {
    background-color: #e2e8f0;
    color: #334155;
}

/* --- Frames & Containers --- */
QFrame#cardFrame {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
}

QFrame[frameShape="4"], QFrame[frameShape="5"] {
    background-color: #e2e8f0;
    border: none;
}

/* --- Scrollbars --- */
QScrollBar:vertical {
    background: transparent;
    width: 8px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #cbd5e1;
    min-height: 24px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: #94a3b8;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
    height: 0px;
}

QScrollBar:horizontal {
    background: transparent;
    height: 8px;
    margin: 0px;
}

QScrollBar::handle:horizontal {
    background: #cbd5e1;
    min-width: 24px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal:hover {
    background: #94a3b8;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;
    width: 0px;
}

/* --- Context Menus & Tooltips --- */
QMenu {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 6px;
}

QMenu::item {
    padding: 6px 22px 6px 12px;
    border-radius: 4px;
    color: #1e293b;
    font-size: 9pt;
}

QMenu::item:selected {
    background-color: #eff6ff;
    color: #2563eb;
}

QMenu::separator {
    height: 1px;
    background-color: #e2e8f0;
    margin: 4px 6px;
}

QToolTip {
    background-color: #ffffff;
    color: #1e293b;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 5px 8px;
    font-size: 8.5pt;
}
"""
