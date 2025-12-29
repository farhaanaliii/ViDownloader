from datetime import datetime

from vidownloader.core.Constants import App, Author
from vidownloader.ui.dialogs import SettingsDialog

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QTextEdit,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QFrame,
    QStatusBar,
    QMessageBox
)
from PyQt5.QtCore import Qt


class HOME_UI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_gui()
        
    
    def init_gui(self):
        self.setWindowTitle(f"{App.NAME} v{App.VERSION} By {Author.NAME}")
        self.resize(800, 600)
        self.setMinimumSize(800, 600)
        self.setWindowIcon(QIcon(f":/icons/{App.ICON}"))
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        
        main_layout = QVBoxLayout(self.main_widget)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(18)
        
        header_layout = QHBoxLayout()
        header_layout.setSpacing(15)
        
        logo_label = QLabel()
        logo_label.setFixedSize(60, 60)
        logo_label.setStyleSheet("background-color: transparent !important; margin-top: 0px !important; margin-bottom: 0px !important;")
        pixmap = QPixmap(f":/icons/{App.ICON}")
        pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        header_layout.addWidget(logo_label)
        
        title_label = QLabel(f"{App.NAME} v{App.VERSION}")
        title_label.setStyleSheet("color: #007bff; margin-left: 5px !important; background-color: transparent !important; font-size: 22pt; font-weight: bold;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        self.settings_button = QPushButton()
        self.settings_button.setText("Settings")
        self.settings_button.setStyleSheet("font-size: 9pt;")
        self.settings_button.setFixedSize(100, 30)
        
        self.settings_button.clicked.connect(self.open_settings)
        header_layout.addWidget(self.settings_button)
        
        main_layout.addLayout(header_layout)
        
        subtitle = QLabel("Download videos easily")
        subtitle.setStyleSheet("color: #6c757d; margin-bottom: 15px; background-color: transparent !important; font-size: 14pt;")
        main_layout.addWidget(subtitle)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #dee2e6; margin: 10px 0;")
        main_layout.addWidget(separator)
        
        instructions = QLabel("Enter video or profile links below, one per line:")
        instructions.setStyleSheet("color: #495057; margin-bottom: 8px; background-color: transparent !important; font-size: 12pt;")
        main_layout.addWidget(instructions)
        
        self.text_area = QTextEdit()
        self.text_area.setPlaceholderText('https://youtube.com/@channel/videos\nhttps://youtube.com/@channel/shorts\nhttps://youtube.com/channel/CHANNEL_ID/videos\nhttps://youtube.com/channel/CHANNEL_ID/shorts\nhttps://youtube.com/watch?v=VIDEO_ID\nhttps://youtube.com/playlist?list=PLAYLIST_ID\n')
        self.text_area.setMinimumHeight(220)
        self.text_area.setAcceptRichText(False)
        main_layout.addWidget(self.text_area)
        
        buttons_layout = self.create_buttons_layout()
        main_layout.addSpacing(10)
        main_layout.addLayout(buttons_layout)
        
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")

    def create_buttons_layout(self):
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        self.import_button = QPushButton('Import')
        self.import_button.setStyleSheet("font-size: 9pt;")
        self.import_button.setMinimumWidth(80)
        self.import_button.setMaximumWidth(100)
        self.import_button.setFixedHeight(30)
        buttons_layout.addWidget(self.import_button)
        
        buttons_layout.addStretch()
        
        self.updates_button = QPushButton("Check update")
        self.updates_button.setFixedSize(115, 30)
        self.updates_button.setStyleSheet("""
            QPushButton {
                color: #28a745;
                font-size: 9pt;
            }
        """)
        buttons_layout.addWidget(self.updates_button)
        
        buttons_layout.addSpacing(5)
        
        self.start_button = QPushButton('Start')
        self.start_button.setMinimumWidth(80)
        self.start_button.setMaximumWidth(100)
        self.start_button.setFixedHeight(30)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                border: none;
                color: white;
                font-size: 9pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0069d9;
            }
            QPushButton:pressed {
                background-color: #0062cc;
            }
        """)
        buttons_layout.addWidget(self.start_button)
        
        return buttons_layout

    def open_settings(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec_()

    def show_about(self):
        QMessageBox.about(self, f"About {App.NAME}", 
        f"""<h2>f"{App.NAME} v{App.VERSION}"</h2>
        <p>A modern application for downloading videos.</p>
        <p>&copy; {datetime.now().year} {App.NAME} Team</p>""")

