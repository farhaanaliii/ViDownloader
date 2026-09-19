from PySide6.QtCore import QRect, QSize, Qt, Signal
from PySide6.QtGui import QColor, QIcon, QPainter
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QStatusBar,
    QStyledItemDelegate,
    QToolBar,
    QTreeWidget,
    QVBoxLayout,
    QWidget,
)

from vidownloader.core.Constants import App, TreeViewColumns
from vidownloader.core.Utils import get_assets_path
from vidownloader.ui.dialogs import ReleaseNotesDialog, SettingsDialog


class ViDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        color = index.data(Qt.BackgroundRole)
        if color:
            painter.save()
            painter.fillRect(option.rect, color)
            painter.restore()

        super().paint(painter, option, index)


class ViProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTextVisible(False)

    def paintEvent(self, event):
        super().paintEvent(event)

        total = self.maximum() - self.minimum()
        current = self.value() - self.minimum()
        fraction = (current / total) if total > 0 else 0.0
        fraction = max(0.0, min(1.0, fraction))

        text = self.text()
        if not text:
            return

        rect = self.rect()
        chunk_w = int(rect.width() * fraction)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)

        font = self.font()
        font.setPointSize(8)
        font.setBold(True)
        painter.setFont(font)

        if chunk_w > 0:
            painter.save()
            painter.setClipRect(QRect(rect.left(), rect.top(), chunk_w, rect.height()))
            painter.setPen(QColor("#ffffff"))
            painter.drawText(rect, Qt.AlignCenter, text)
            painter.restore()

        if chunk_w < rect.width():
            painter.save()
            painter.setClipRect(QRect(rect.left() + chunk_w, rect.top(), rect.width() - chunk_w, rect.height()))
            painter.setPen(QColor("#1e293b"))
            painter.drawText(rect, Qt.AlignCenter, text)
            painter.restore()

        painter.end()


class MAIN_UI(QMainWindow):
    loaded = Signal(dict)

    def __init__(self):
        super().__init__()
        self.init_gui()

    def init_gui(self):
        self.setWindowTitle(f"{App.NAME} v{App.VERSION}")
        self.setWindowIcon(QIcon(get_assets_path(f"icons/{App.ICON}")))
        self.showMaximized()
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        toolbar = QToolBar()
        toolbar.setIconSize(QSize(24, 24))
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        back_button = QPushButton("Back")
        back_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        back_button.setMinimumWidth(80)
        back_button.setMaximumWidth(120)
        back_button.setFixedHeight(32)
        back_button.clicked.connect(self.go_back)
        toolbar.addWidget(back_button)

        title_label = QLabel(f"  {App.NAME}")
        title_label.setStyleSheet("color: #2563eb; font-size: 13pt; font-weight: bold;")
        toolbar.addWidget(title_label)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer)

        release_notes_button = QPushButton("Release Notes")
        release_notes_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        release_notes_button.setMinimumWidth(110)
        release_notes_button.setFixedHeight(32)
        release_notes_button.clicked.connect(self.show_release_notes)
        toolbar.addWidget(release_notes_button)

        settings_button = QPushButton("Settings")
        settings_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        settings_button.setMinimumWidth(90)
        settings_button.setFixedHeight(32)
        settings_button.clicked.connect(self.open_settings)
        toolbar.addWidget(settings_button)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        main_layout = QVBoxLayout(self.main_widget)
        main_layout.setContentsMargins(25, 20, 25, 20)
        main_layout.setSpacing(14)

        status_layout = QHBoxLayout()
        status_layout.setSpacing(15)

        self.status_label = QLabel("Ready to scrape videos")
        self.status_label.setStyleSheet("color: #059669; font-weight: 600; font-size: 10pt;")
        status_layout.addWidget(self.status_label)

        status_layout.addStretch()

        self.progress_bar = ViProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.progress_bar.setMinimumWidth(150)
        self.progress_bar.setMaximumWidth(360)
        self.progress_bar.setFormat("%p% - %v of %m")
        status_layout.addWidget(self.progress_bar)

        main_layout.addLayout(status_layout)

        self.tree_widget = QTreeWidget()
        self.tree_widget.setItemDelegate(ViDelegate())
        self.tree_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tree_widget.setSelectionMode(QTreeWidget.ExtendedSelection)
        self.tree_widget.setAlternatingRowColors(True)
        self.tree_widget.setMinimumHeight(300)
        self.tree_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tree_widget.setColumnCount(8)
        self.tree_widget.setHeaderLabels(
            [
                "No #",
                "Caption",
                "Progress",
                "Status",
                "Username",
                "Views",
                "ID",
                "Size",
                "Duration",
            ]
        )
        self.tree_widget.setUniformRowHeights(True)
        header = self.tree_widget.header()
        header.setSectionResizeMode(QHeaderView.Interactive)

        self.tree_widget.setColumnWidth(TreeViewColumns.NO, 80)
        self.tree_widget.setColumnWidth(TreeViewColumns.PROGRESS, 95)
        self.tree_widget.setColumnWidth(TreeViewColumns.STATUS, 110)
        self.tree_widget.setColumnWidth(TreeViewColumns.USERNAME, 130)
        self.tree_widget.setColumnWidth(TreeViewColumns.VIEWS, 90)
        self.tree_widget.setColumnWidth(TreeViewColumns.ID, 140)
        self.tree_widget.setColumnWidth(TreeViewColumns.SIZE, 95)
        self.tree_widget.setColumnWidth(TreeViewColumns.DURATION, 90)

        header.setSectionResizeMode(TreeViewColumns.CAPTION, QHeaderView.Stretch)

        main_layout.addWidget(self.tree_widget)

        buttons_frame = QFrame()
        buttons_frame.setObjectName("cardFrame")
        buttons_layout = QHBoxLayout(buttons_frame)
        buttons_layout.setContentsMargins(18, 14, 18, 14)
        buttons_layout.setSpacing(18)

        selection_layout = QVBoxLayout()
        selection_layout.setSpacing(8)
        selection_label = QLabel("Selection")
        selection_label.setStyleSheet("color: #334155; font-size: 9.5pt; font-weight: 600;")
        selection_layout.addWidget(selection_label)

        selection_buttons = QHBoxLayout()
        selection_buttons.setSpacing(8)
        self.select_all_button = QPushButton("All")
        self.select_all_button.setFixedHeight(32)
        self.select_all_button.setMinimumWidth(75)
        selection_buttons.addWidget(self.select_all_button)

        self.deselect_button = QPushButton("None")
        self.deselect_button.setFixedHeight(32)
        self.deselect_button.setMinimumWidth(75)
        selection_buttons.addWidget(self.deselect_button)

        selection_layout.addLayout(selection_buttons)
        buttons_layout.addLayout(selection_layout)

        v_separator1 = QFrame()
        v_separator1.setFrameShape(QFrame.VLine)
        v_separator1.setFrameShadow(QFrame.Plain)
        buttons_layout.addWidget(v_separator1)

        download_layout = QVBoxLayout()
        download_layout.setSpacing(8)
        download_label = QLabel("Download Controls")
        download_label.setStyleSheet("color: #334155; font-size: 9.5pt; font-weight: 600;")
        download_layout.addWidget(download_label)

        download_buttons = QHBoxLayout()
        download_buttons.setSpacing(8)

        self.download_button = QPushButton("Download")
        self.download_button.setProperty("primary", "true")
        self.download_button.setEnabled(False)
        self.download_button.setFixedHeight(32)
        self.download_button.setMinimumWidth(95)
        download_buttons.addWidget(self.download_button)

        self.pause_button = QPushButton("Pause")
        self.pause_button.setEnabled(False)
        self.pause_button.setFixedHeight(32)
        self.pause_button.setMinimumWidth(80)
        download_buttons.addWidget(self.pause_button)

        self.resume_button = QPushButton("Resume")
        self.resume_button.setEnabled(False)
        self.resume_button.setFixedHeight(32)
        self.resume_button.setMinimumWidth(80)
        download_buttons.addWidget(self.resume_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setProperty("danger", "true")
        self.stop_button.setEnabled(False)
        self.stop_button.setFixedHeight(32)
        self.stop_button.setMinimumWidth(80)
        download_buttons.addWidget(self.stop_button)

        download_layout.addLayout(download_buttons)
        buttons_layout.addLayout(download_layout)

        v_separator2 = QFrame()
        v_separator2.setFrameShape(QFrame.VLine)
        v_separator2.setFrameShadow(QFrame.Plain)
        buttons_layout.addWidget(v_separator2)

        export_layout = QVBoxLayout()
        export_layout.setSpacing(8)
        export_label = QLabel("Data Management")
        export_label.setStyleSheet("color: #334155; font-size: 9.5pt; font-weight: 600;")
        export_layout.addWidget(export_label)

        self.export_button = QPushButton("Export")
        self.export_button.setFixedHeight(32)
        self.export_button.setMinimumWidth(85)
        export_layout.addWidget(self.export_button)

        buttons_layout.addLayout(export_layout)

        main_layout.addWidget(buttons_frame)

    def go_back(self):
        pass  # Implemented in MainWindow

    def show_release_notes(self):
        release_notes_dialog = ReleaseNotesDialog(self)
        release_notes_dialog.exec_()

    def open_settings(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec_()
