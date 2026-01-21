from vidownloader.core.Constants import FileName, PlaylistOrganization, SingleVideoOrganization
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


class ReleaseNotesDialog(QDialog):
    """Dialog for displaying release notes and changelog."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Release Notes")
        self.setMinimumSize(700, 600)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        title = QLabel("Release History")
        title.setStyleSheet("color: #007bff; margin-bottom: 8px; font-size: 12pt; font-weight: bold;")
        main_layout.addWidget(title)
        
        self.release_browser = QTextBrowser()
        self.release_browser.setStyleSheet("padding: 15px;")
        self.release_browser.setHtml("""
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
        
        <h2>Version 1.0.0-beta2 <span class="date">(Current - January 2026)</span></h2>
        <p><span class="beta">⚠ BETA:</span> This version is functional but may have rough edges. Your feedback helps!</p>
        
        <h3>✨ New Features</h3>
        <ul>
            <li><span class="new">NEW:</span> Flexible video organization system
                <ul style="margin-top: 5px;">
                    <li>Playlists: Group by playlist name or uploader</li>
                    <li>Single videos: Group in dedicated folder or by uploader</li>
                    <li>Configurable organization settings in Settings dialog</li>
                </ul>
            </li>
            <li><span class="new">NEW:</span> Real-time download progress tracking</li>
            <li><span class="new">NEW:</span> Video duration display (HH:MM:SS format)</li>
            <li><span class="new">NEW:</span> Video file size display after download completion</li>
            <li><span class="new">NEW:</span> Download button state management (prevents duplicate downloads)</li>
        </ul>
        
        <h3>🔧 Improvements</h3>
        <ul>
            <li><span class="improved">IMPROVED:</span> Better error handling for video metadata</li>
            <li><span class="improved">IMPROVED:</span> Optimized event handling (reduced duplicate lookups)</li>
            <li><span class="improved">IMPROVED:</span> Consolidated video data storage in tree items</li>
            <li><span class="improved">IMPROVED:</span> Enhanced YouTube parser for metadata extraction</li>
        </ul>
        
        <h3>🐛 Bug Fixes</h3>
        <ul>
            <li><span class="fixed">FIXED:</span> Video size display error handling</li>
            <li><span class="fixed">FIXED:</span> Event type checking improvements</li>
            <li><span class="fixed">FIXED:</span> Various stability improvements</li>
        </ul>
        
        <hr style="margin: 20px 0; border: 1px solid #e0e0e0;">
        
        <h2>Version 1.0.0-beta <span class="date">(December 2025)</span></h2>
        
        <h3>Initial Beta Features</h3>
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
        
        main_layout.addWidget(self.release_browser)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        close_button = QPushButton("Close")
        close_button.setMinimumWidth(100)
        close_button.setStyleSheet("background-color: #007bff; color: white;")
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)
        
        main_layout.addLayout(button_layout)


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
        
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine)
        separator2.setFrameShadow(QFrame.Sunken)
        separator2.setStyleSheet("background-color: #e0e0e0;")
        general_layout.addRow("", separator2)
        
        organization_title = QLabel("Organization Settings")
        organization_title.setStyleSheet("color: #007bff; margin-top: 12px; margin-bottom: 8px; font-size: 12pt; font-weight: bold;")
        general_layout.addRow("", organization_title)
        
        self.playlist_org = QComboBox()
        self.playlist_org.addItem("Group by Playlist Name", PlaylistOrganization.BY_PLAYLIST)
        self.playlist_org.addItem("Group by Uploader", PlaylistOrganization.BY_UPLOADER)
        self.playlist_org.setFixedHeight(25)
        index = self.playlist_org.findData(VSettings.get_playlist_organization())
        if index >= 0:
            self.playlist_org.setCurrentIndex(index)
        general_layout.addRow("Playlist Organization", self.playlist_org)
        
        self.single_video_org = QComboBox()
        self.single_video_org.addItem("Group in Singles Folder", SingleVideoOrganization.GROUP_SINGLES)
        self.single_video_org.addItem("Group by Uploader", SingleVideoOrganization.BY_UPLOADER)
        self.single_video_org.setFixedHeight(25)
        index = self.single_video_org.findData(VSettings.get_single_video_organization())
        if index >= 0:
            self.single_video_org.setCurrentIndex(index)
        general_layout.addRow("Single Video Organization", self.single_video_org)
        
        tab_widget.addTab(general_tab, "General")
        
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
        VSettings.set_playlist_organization(self.playlist_org.currentData())
        VSettings.set_single_video_organization(self.single_video_org.currentData())
        
        super().accept()
