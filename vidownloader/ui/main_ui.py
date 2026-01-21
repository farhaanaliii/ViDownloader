from vidownloader.core.Constants import App
from vidownloader.ui.dialogs import SettingsDialog, ReleaseNotesDialog

from PyQt5.QtCore import QSize, pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QStatusBar,
    QToolBar,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QSizePolicy,
    QProgressBar,
    QTreeWidget,
    QFrame,
    QHeaderView
)
from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtCore import Qt

class ViDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        color = index.data(Qt.BackgroundRole)
        if color:
            painter.save()
            painter.fillRect(option.rect, color)
            painter.restore()
        
        super().paint(painter, option, index)

class MAIN_UI(QMainWindow):
    loaded = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.init_gui()

    def apply_font(self, widget: QWidget, size: int, bold: bool = False):
        font = widget.font()
        font.setPointSize(size)
        font.setBold(bold)
        widget.setFont(font)

    def init_gui(self):
        self.setWindowTitle(f"{App.NAME} v{App.VERSION}")
        self.setWindowIcon(QIcon(f":/icons/{App.ICON}"))
        self.showMaximized()
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(24, 24))
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        back_button = QPushButton("Back")
        self.apply_font(back_button, 9)
        back_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        back_button.setMinimumWidth(80)
        back_button.setMaximumWidth(140)
        back_button.setMinimumHeight(28)
        back_button.setMaximumHeight(40)
        back_button.clicked.connect(self.go_back)
        toolbar.addWidget(back_button)
        
        title_label = QLabel(f"  {App.NAME}")
        self.apply_font(title_label, 16, True)
        title_label.setStyleSheet("color: #007bff;")
        toolbar.addWidget(title_label)
        
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer)
        
        release_notes_button = QPushButton("Release Notes")
        self.apply_font(release_notes_button, 9)
        release_notes_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        release_notes_button.setMinimumWidth(80)
        release_notes_button.setMaximumWidth(140)
        release_notes_button.setMinimumHeight(28)
        release_notes_button.setMaximumHeight(40)
        release_notes_button.clicked.connect(self.show_release_notes)
        toolbar.addWidget(release_notes_button)
        
        settings_button = QPushButton("Settings")
        self.apply_font(settings_button, 9)
        settings_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        settings_button.setMinimumWidth(80)
        settings_button.setMaximumWidth(140)
        settings_button.setMinimumHeight(28)
        settings_button.setMaximumHeight(40)
        settings_button.clicked.connect(self.open_settings)
        toolbar.addWidget(settings_button)
        
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        
        main_layout = QVBoxLayout(self.main_widget)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(18)
        
        status_layout = QHBoxLayout()
        status_layout.setSpacing(15)
        
        self.status_label = QLabel("Ready to scrape videos")
        self.apply_font(self.status_label, 10)
        self.status_label.setStyleSheet("color: #28a745; font-weight: bold;")
        status_layout.addWidget(self.status_label)
        
        status_layout.addStretch()
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.progress_bar.setMinimumWidth(120)
        self.progress_bar.setMaximumWidth(400)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p% - %v of %m")
        status_layout.addWidget(self.progress_bar)
        
        main_layout.addLayout(status_layout)
        
        self.tree_widget = QTreeWidget()
        self.tree_widget.setItemDelegate(ViDelegate())
        self.tree_widget.setMinimumHeight(300)
        self.tree_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tree_widget.setColumnCount(8)
        self.tree_widget.setHeaderLabels(['', 'No #', 'Caption', 'Progress', 'Status', 'Username', 'ID', 'Size', 'Duration'])
        self.tree_widget.setAlternatingRowColors(True)
        self.tree_widget.setSelectionMode(QTreeWidget.ExtendedSelection)
        self.tree_widget.setUniformRowHeights(True)
        main_layout.addWidget(self.tree_widget)
        
        buttons_frame = QFrame()
        buttons_frame.setFrameShape(QFrame.StyledPanel)
        buttons_frame.setStyleSheet("""
            QPushButton {
                min-width: 80px;
                min-height: 28px;
                max-width: 100px;
                border-radius: 4px;
                font-size: 9pt;
            }
        """)
        buttons_layout = QHBoxLayout(buttons_frame)
        buttons_layout.setContentsMargins(20, 15, 20, 15)
        buttons_layout.setSpacing(20)
        
        selection_layout = QVBoxLayout()
        selection_label = QLabel("Selection")
        self.apply_font(selection_label, 11, True)
        selection_layout.addWidget(selection_label)
        
        selection_buttons = QHBoxLayout()
        selection_buttons.setSpacing(10)
        self.select_all_button = QPushButton('All')
        self.apply_font(self.select_all_button, 9)
        self.select_all_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        selection_buttons.addWidget(self.select_all_button)
        
        self.deselect_button = QPushButton('None')
        self.apply_font(self.deselect_button, 9)
        self.deselect_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        selection_buttons.addWidget(self.deselect_button)
        
        selection_layout.addLayout(selection_buttons)
        buttons_layout.addLayout(selection_layout)
        
        v_separator1 = QFrame()
        v_separator1.setFrameShape(QFrame.VLine)
        v_separator1.setFrameShadow(QFrame.Sunken)
        v_separator1.setStyleSheet("background-color: #dee2e6;")
        buttons_layout.addWidget(v_separator1)
        
        download_layout = QVBoxLayout()
        download_label = QLabel("Download Controls")
        self.apply_font(download_label, 11, True)
        download_layout.addWidget(download_label)
        
        download_buttons = QHBoxLayout()
        download_buttons.setSpacing(10)
        
        self.download_button = QPushButton('Download')
        self.apply_font(self.download_button, 9)
        self.download_button.setEnabled(False)
        self.download_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                border: none;
                color: white;
            }
            QPushButton:hover {
                background-color: #0069d9;
            }
            QPushButton:pressed {
                background-color: #0062cc;
            }
        """)
        self.download_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        download_buttons.addWidget(self.download_button)
        
        self.pause_button = QPushButton('Pause')
        self.apply_font(self.pause_button, 9)
        self.pause_button.setEnabled(False)
        self.pause_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        download_buttons.addWidget(self.pause_button)
        
        self.resume_button = QPushButton('Resume')
        self.apply_font(self.resume_button, 9)
        self.resume_button.setEnabled(False)
        self.resume_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        download_buttons.addWidget(self.resume_button)
        
        self.stop_button = QPushButton('Stop')
        self.apply_font(self.stop_button, 9)
        self.stop_button.setEnabled(False)
        self.stop_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        download_buttons.addWidget(self.stop_button)
        
        download_layout.addLayout(download_buttons)
        buttons_layout.addLayout(download_layout)
        
        v_separator2 = QFrame()
        v_separator2.setFrameShape(QFrame.VLine)
        v_separator2.setFrameShadow(QFrame.Sunken)
        buttons_layout.addWidget(v_separator2)
        
        export_layout = QVBoxLayout()
        export_label = QLabel("Data Management")
        self.apply_font(export_label, 11, True)
        export_layout.addWidget(export_label)
        
        self.export_button = QPushButton('Export')
        self.apply_font(self.export_button, 9)
        self.export_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        export_layout.addWidget(self.export_button)
        
        buttons_layout.addLayout(export_layout)
        
        main_layout.addWidget(buttons_frame)
        
        header = self.tree_widget.header()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        header.setSectionResizeMode(5, QHeaderView.Stretch)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)
    
    def go_back(self):
        pass # TODO: Implement go back functionality
    
    def show_release_notes(self):
        release_notes_dialog = ReleaseNotesDialog(self)
        release_notes_dialog.exec_()
    
    def open_settings(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec_()
