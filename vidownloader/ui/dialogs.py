from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFileDialog,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QTabWidget,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from vidownloader.core import VSettings
from vidownloader.core.Constants import (
    FileName,
    PlaylistOrganization,
    SingleVideoOrganization,
)


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
        title.setStyleSheet(
            "color: #007bff; margin-bottom: 8px; font-size: 12pt; font-weight: bold;"
        )
        main_layout.addWidget(title)

        self.release_browser = QTextBrowser()
        self.release_browser.setStyleSheet("padding: 15px;")
        self.release_browser.setHtml("""
        <style>
            h2 { color: #007bff; margin-top: 20px; }
            h3 { color: #6c757d; margin-top: 15px; font-size: 11pt; }
            ul { margin-left: 20px; }
            li { margin-bottom: 8px; }
            .date { color: #6c757d; }
            .pre { color: #fd7e14; font-weight: bold; }
            .new { color: #28a745; }
            .improved { color: #fd7e14; }
            .fixed { color: #dc3545; }
        </style>

        <h2>v0.5.0 <span class="date">(July 2026)</span></h2>
        <p><span class="pre">&#9888; PRE-RELEASE:</span> This version is functional but expect rough edges. Your feedback helps!</p>

        <h3>&#10024; New Features</h3>
        <ul>
            <li><span class="new">NEW:</span> Complete migration from PyQt5 to PySide6 (Qt6) bindings</li>
            <li><span class="new">NEW:</span> Automated Python package publishing to PyPI via GitHub Actions</li>
        </ul>

        <h3>&#128027; Security & Bug Fixes</h3>
        <ul>
            <li><span class="fixed">FIXED:</span> Path traversal vulnerability in download path construction</li>
            <li><span class="fixed">FIXED:</span> Duplicate signal connection on stop button</li>
            <li><span class="fixed">FIXED:</span> Suppressed yt-dlp progress bar output in GUI threads</li>
        </ul>

        <h3>&#128295; Improvements & Performance</h3>
        <ul>
            <li><span class="improved">IMPROVED:</span> O(1) dictionary lookup for tree widget items replacing O(n) traversal</li>
            <li><span class="improved">IMPROVED:</span> Simplified DownloaderWorker lifecycle and clean thread interruption</li>
            <li><span class="improved">IMPROVED:</span> Scraper stop signal handling with stop_checker callback</li>
            <li><span class="improved">IMPROVED:</span> Added XVFB and Qt6 dependencies for CI testing</li>
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
        section_title.setStyleSheet(
            "color: #007bff; margin-bottom: 8px; font-size: 12pt; font-weight: bold;"
        )
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
        file_title.setStyleSheet(
            "color: #007bff; margin-top: 12px; margin-bottom: 8px; font-size: 12pt; font-weight: bold;"
        )
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
        organization_title.setStyleSheet(
            "color: #007bff; margin-top: 12px; margin-bottom: 8px; font-size: 12pt; font-weight: bold;"
        )
        general_layout.addRow("", organization_title)

        self.playlist_org = QComboBox()
        self.playlist_org.addItem(
            "Group by Playlist Name", PlaylistOrganization.BY_PLAYLIST
        )
        self.playlist_org.addItem("Group by Uploader", PlaylistOrganization.BY_UPLOADER)
        self.playlist_org.setFixedHeight(25)
        index = self.playlist_org.findData(VSettings.get_playlist_organization())
        if index >= 0:
            self.playlist_org.setCurrentIndex(index)
        general_layout.addRow("Playlist Organization", self.playlist_org)

        self.single_video_org = QComboBox()
        self.single_video_org.addItem(
            "Group in Singles Folder", SingleVideoOrganization.GROUP_SINGLES
        )
        self.single_video_org.addItem(
            "Group by Uploader", SingleVideoOrganization.BY_UPLOADER
        )
        self.single_video_org.setFixedHeight(25)
        index = self.single_video_org.findData(
            VSettings.get_single_video_organization()
        )
        if index >= 0:
            self.single_video_org.setCurrentIndex(index)
        general_layout.addRow("Single Video Organization", self.single_video_org)

        advanced_tab = QWidget()
        advanced_layout = QFormLayout(advanced_tab)
        advanced_layout.setContentsMargins(15, 15, 15, 15)
        advanced_layout.setSpacing(12)
        advanced_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        advanced_layout.setLabelAlignment(Qt.AlignRight)
        advanced_layout.setRowWrapPolicy(QFormLayout.DontWrapRows)

        section_title = QLabel("Advanced Settings")
        section_title.setStyleSheet("color: #007bff; margin-bottom: 8px; font-size: 12pt; font-weight: bold;")
        advanced_layout.addRow("", section_title)
        
        self.cookies_browser_selector = QComboBox(self)
        self.cookies_browser_selector.addItems(["None", "Chrome", "Firefox", "Edge", "Brave", "Opera", "Vivaldi", "Chromium"])
        
        self.cookies_profile = QLineEdit()
        self.cookies_profile.setPlaceholderText("Profile name or path (optional)")

        self.cookies_profile_browse = QPushButton("Browse...")
        self.cookies_profile_browse.setMaximumWidth(100)
        self.cookies_profile_browse.clicked.connect(self.browse_cookies_profile)

        browser = VSettings.get_cookies_browser()
        profile = VSettings.get_cookies_profile()
        
        index = self.cookies_browser_selector.findText(browser.capitalize())
        self.cookies_browser_selector.setCurrentIndex(index if index >= 0 else 0)
        self.cookies_browser_selector.currentTextChanged.connect(self.update_cookies_browser)
                
        self.cookies_profile.setText(profile)
        self.update_cookies_browser()

        cookies_layout = QHBoxLayout()
        cookies_layout.addWidget(self.cookies_browser_selector)
        cookies_layout.addWidget(self.cookies_profile)
        cookies_layout.addWidget(self.cookies_profile_browse)
        advanced_layout.addRow("Cookies Browser", cookies_layout)

        tab_widget.addTab(general_tab, "General")
        tab_widget.addTab(advanced_tab, "Advanced")

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

    def browse_cookies_profile(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Browser Profile Folder")
        if folder:
            self.cookies_profile.setText(folder)

    def update_cookies_browser(self):
        enabled = self.cookies_browser_selector.currentText() != "None"
        self.cookies_profile.setEnabled(enabled)
        self.cookies_profile_browse.setEnabled(enabled)

    def accept(self):
        VSettings.set_download_location(self.download_location.text().strip())
        VSettings.set_export_location(self.export_location.text().strip())
        VSettings.set_file_naming_mode(self.caption_setting.currentData())
        VSettings.set_download_threads(self.threads.value())
        VSettings.set_playlist_organization(self.playlist_org.currentData())
        VSettings.set_single_video_organization(self.single_video_org.currentData())
        
        browser = self.cookies_browser_selector.currentText()
        VSettings.set_cookies_browser("" if browser == "None" else browser.lower())
        VSettings.set_cookies_profile("" if browser == "None" else self.cookies_profile.text().strip())

        super().accept()
