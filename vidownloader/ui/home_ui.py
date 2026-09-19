from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStatusBar,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from vidownloader.core.Constants import App, Author
from vidownloader.core.Utils import get_assets_path
from vidownloader.ui.dialogs import ReleaseNotesDialog, SettingsDialog


class HOME_UI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_gui()

    def init_gui(self):
        self.setWindowTitle(f"{App.NAME} v{App.VERSION} By {Author.NAME}")
        self.resize(800, 600)
        self.setMinimumSize(800, 600)
        self.setWindowIcon(QIcon(get_assets_path(f"icons/{App.ICON}")))
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        main_layout = QVBoxLayout(self.main_widget)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(18)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(15)

        logo_label = QLabel()
        logo_label.setFixedSize(56, 56)
        pixmap = QPixmap(get_assets_path(f"icons/{App.ICON}"))
        pixmap = pixmap.scaled(56, 56, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        header_layout.addWidget(logo_label)

        title_label = QLabel(f"{App.NAME} v{App.VERSION}")
        title_label.setStyleSheet("color: #2563eb; font-size: 20pt; font-weight: bold;")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        self.settings_button = QPushButton("Settings")
        self.settings_button.setFixedSize(96, 32)
        self.settings_button.clicked.connect(self.open_settings)
        header_layout.addWidget(self.settings_button)

        main_layout.addLayout(header_layout)

        subtitle = QLabel("Download videos, playlists, and channels effortlessly.")
        subtitle.setStyleSheet("color: #64748b; font-size: 11pt;")
        main_layout.addWidget(subtitle)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Plain)
        main_layout.addWidget(separator)

        instructions = QLabel("Enter video, shorts, playlist, or channel links (one per line):")
        instructions.setStyleSheet("color: #334155; font-size: 10pt; font-weight: 600;")
        main_layout.addWidget(instructions)

        self.text_area = QTextEdit()
        self.text_area.setPlaceholderText(
            "https://youtube.com/@channel/videos\nhttps://youtube.com/@channel/shorts\nhttps://youtube.com/channel/CHANNEL_ID/videos\nhttps://youtube.com/channel/CHANNEL_ID/shorts\nhttps://youtube.com/watch?v=VIDEO_ID\nhttps://youtube.com/playlist?list=PLAYLIST_ID\n"
        )
        self.text_area.setMinimumHeight(220)
        self.text_area.setAcceptRichText(False)
        main_layout.addWidget(self.text_area)

        buttons_layout = self.create_buttons_layout()
        main_layout.addSpacing(6)
        main_layout.addLayout(buttons_layout)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")

    def create_buttons_layout(self):
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)

        self.import_button = QPushButton("Import")
        self.import_button.setMinimumWidth(85)
        self.import_button.setFixedHeight(32)
        buttons_layout.addWidget(self.import_button)

        buttons_layout.addStretch()

        self.updates_button = QPushButton("Check Update")
        self.updates_button.setProperty("success", "true")
        self.updates_button.setFixedSize(115, 32)
        buttons_layout.addWidget(self.updates_button)

        self.release_notes_button = QPushButton("Release Notes")
        self.release_notes_button.setFixedSize(115, 32)
        self.release_notes_button.clicked.connect(self.show_release_notes)
        buttons_layout.addWidget(self.release_notes_button)

        self.start_button = QPushButton("Start")
        self.start_button.setProperty("primary", "true")
        self.start_button.setMinimumWidth(90)
        self.start_button.setFixedHeight(32)
        buttons_layout.addWidget(self.start_button)

        return buttons_layout

    def open_settings(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec_()

    def show_release_notes(self):
        release_notes_dialog = ReleaseNotesDialog(self)
        release_notes_dialog.exec_()

    def show_about(self):
        QMessageBox.about(
            self,
            f"About {App.NAME}",
            f"""<h2>{App.NAME} v{App.VERSION}</h2>
        <p>A modern application for downloading videos.</p>
        <p>&copy; {datetime.now().year} {Author.NAME}</p>""",
        )
