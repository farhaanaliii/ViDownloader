from vidownloader.core.Constants import FileName
from vidownloader.core import VSettings

from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QTabWidget,
    QWidget,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QFrame,
    QComboBox,
    QSpinBox,
    QTextBrowser,
    QFileDialog
)
from PyQt5.QtCore import Qt


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumSize(650, 500)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        
        tab_widget = QTabWidget()
        tab_widget.setDocumentMode(True)
        
        general_tab = QWidget()
        general_layout = QFormLayout(general_tab)
        general_layout.setContentsMargins(15, 15, 15, 15)
        general_layout.setSpacing(12)
        general_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        general_layout.setLabelAlignment(Qt.AlignRight)
        general_layout.setRowWrapPolicy(QFormLayout.DontWrapRows)
        
        section_title = QLabel("Download Settings")
        section_title.setStyleSheet("color: #007bff; margin-bottom: 8px; font-size: 12pt; font-weight: bold;")
        general_layout.addRow("", section_title)
        
        self.download_location = QLineEdit()
        self.download_location.setText(VSettings.get_download_location())
        browse_button = QPushButton("Browse...")
        browse_button.setMaximumWidth(100)
        browse_button.clicked.connect(self.browse_download_location)
        
        download_layout = QHBoxLayout()
        download_layout.addWidget(self.download_location)
        download_layout.addWidget(browse_button)
        
        general_layout.addRow("Download Location", download_layout)
        
        self.export_location = QLineEdit()
        self.export_location.setText(VSettings.get_export_location())
        export_browse_button = QPushButton("Browse...")
        export_browse_button.setMaximumWidth(100)
        export_browse_button.clicked.connect(self.browse_export_location)
        
        export_layout = QHBoxLayout()
        export_layout.addWidget(self.export_location)
        export_layout.addWidget(export_browse_button)
        
        general_layout.addRow("Export Links Location", export_layout)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #e0e0e0;")
        general_layout.addRow("", separator)
        
        file_title = QLabel("File Settings")
        file_title.setStyleSheet("color: #007bff; margin-top: 12px; margin-bottom: 8px; font-size: 12pt; font-weight: bold;")
        general_layout.addRow("", file_title)
        
        self.caption_setting = QComboBox()
        self.caption_setting.addItem("Use video title", FileName.CAPTION)
        self.caption_setting.addItem("Use video ID", FileName.VIDEO_ID)
        self.caption_setting.addItem("Use random name", FileName.RANDOM)
        self.caption_setting.setFixedHeight(25)
        
        index = self.caption_setting.findData(VSettings.get_file_naming_mode())
        if index >= 0:
            self.caption_setting.setCurrentIndex(index)
        
        general_layout.addRow("File Naming", self.caption_setting)
        
        self.threads = QSpinBox()
        self.threads.setRange(1, 10)
        self.threads.setValue(VSettings.get_download_threads())
        self.threads.setFixedHeight(25)
        general_layout.addRow("Download Threads", self.threads)
        
        tab_widget.addTab(general_tab, "General")
        
        changelog_tab = QWidget()
        changelog_layout = QVBoxLayout(changelog_tab)
        changelog_layout.setContentsMargins(20, 20, 20, 20)
        changelog_layout.setSpacing(15)
        
        changelog_title = QLabel("Release History")
        changelog_title.setStyleSheet("color: #007bff; margin-bottom: 8px; font-size: 12pt; font-weight: bold;")
        changelog_layout.addWidget(changelog_title)
        
        self.changelog_browser = QTextBrowser()
        self.changelog_browser.setStyleSheet("padding: 15px;")
        self.changelog_browser.setHtml("""
        <style>
            h2 { color: #007bff; margin-top: 20px; }
            h3 { color: #6c757d; margin-top: 15px; font-size: 11pt; }
            ul { margin-left: 20px; }
            li { margin-bottom: 8px; }
            .version { color: #28a745; font-weight: bold; }
            .date { color: #6c757d; }
            .beta { color: #fd7e14; font-weight: bold; }
            .new { color: #28a745; }
            .improved { color: #fd7e14; }
            .fixed { color: #dc3545; }
        </style>
        
        <h2>Version 1.0.0-beta <span class="date">(Current - December 2025)</span></h2>
        <p><span class="beta">⚠ BETA:</span> This version is functional but may have rough edges. Your feedback helps!</p>
        
        <h3>Current Features</h3>
        <ul>
            <li><span class="new">NEW:</span> YouTube video & shorts scraping from channels</li>
            <li><span class="new">NEW:</span> Single video/short direct downloads</li>
            <li><span class="new">NEW:</span> Playlist scraping</li>
            <li><span class="new">NEW:</span> Multi-threaded bulk downloads (1-10 concurrent threads)</li>
            <li><span class="new">NEW:</span> Pause/Resume download capability</li>
            <li><span class="new">NEW:</span> Export/Import video lists (.viio format)</li>
            <li><span class="new">NEW:</span> Flexible file naming (title, video ID, or random)</li>
            <li><span class="new">NEW:</span> Modern PyQt5 interface with real-time progress tracking</li>
            <li><span class="new">NEW:</span> Configurable download and export directories</li>
        </ul>
        
        <h3>Coming Soon</h3>
        <ul>
            <li><span class="new">NEW:</span> Quality selection (720p, 1080p, 4K)</li>
            <li><span class="new">NEW:</span> Advanced filtering and search in video lists</li>
            <li><span class="new">NEW:</span> Download history and statistics</li>
            <li><span class="improved">IMPROVED:</span> Better performance and memory optimization</li>
            <li><span class="improved">IMPROVED:</span> Enhanced error handling and retry logic</li>
        </ul>
        """)
        
        changelog_layout.addWidget(self.changelog_browser)
        tab_widget.addTab(changelog_tab, "Changelog")
        
        main_layout.addWidget(tab_widget)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        button_layout.addStretch()
        
        self.back_button = QPushButton("Save and Close")
        self.back_button.setMinimumWidth(150)
        self.back_button.setStyleSheet("background-color: #007bff; color: white;")
        self.back_button.clicked.connect(self.accept)
        
        button_layout.addWidget(self.back_button)
        
        main_layout.addLayout(button_layout)
    
    def browse_download_location(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Download Folder")
        if folder:
            self.download_location.setText(folder)
    
    def browse_export_location(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Export Folder")
        if folder:
            self.export_location.setText(folder)
    
    def accept(self):
        VSettings.set_download_location(self.download_location.text().strip())
        VSettings.set_export_location(self.export_location.text().strip())
        VSettings.set_file_naming_mode(self.caption_setting.currentData())
        VSettings.set_download_threads(self.threads.value())
        
        super().accept()
