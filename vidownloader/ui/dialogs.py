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
    OutputFormat,
    PlaylistOrganization,
    SingleVideoOrganization,
    VideoQuality,
)


class ReleaseNotesDialog(QDialog):
    """Dialog for displaying release notes and changelog."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Release Notes")
        self.setMinimumSize(700, 560)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(22, 22, 22, 22)
        main_layout.setSpacing(14)

        title = QLabel("Release History")
        title.setStyleSheet("color: #2563eb; font-size: 13pt; font-weight: bold; margin-bottom: 2px;")
        main_layout.addWidget(title)

        self.release_browser = QTextBrowser()
        self.release_browser.setHtml("""
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; color: #1e293b; }
            h2 { color: #1e293b; margin-top: 14px; margin-bottom: 6px; font-size: 13pt; font-weight: 600; }
            h3 { color: #475569; margin-top: 14px; margin-bottom: 6px; font-size: 10.5pt; font-weight: 600; }
            p { color: #475569; font-size: 9.5pt; margin-top: 4px; margin-bottom: 8px; }
            ul { margin-left: 18px; margin-top: 4px; }
            li { margin-bottom: 6px; color: #334155; font-size: 9.5pt; line-height: 1.4; }
            .date { color: #94a3b8; font-size: 9pt; font-weight: normal; }
            .pre { color: #2563eb; font-weight: 600; }
            .new { color: #059669; font-weight: 600; }
            .improved { color: #d97706; font-weight: 600; }
            .fixed { color: #dc2626; font-weight: 600; }
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
        close_button.setProperty("primary", "true")
        close_button.setMinimumWidth(100)
        close_button.setFixedHeight(32)
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)

        main_layout.addLayout(button_layout)


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumSize(650, 520)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(14)

        tab_widget = QTabWidget()

        general_tab = QWidget()
        general_layout = QFormLayout(general_tab)
        general_layout.setContentsMargins(18, 18, 18, 18)
        general_layout.setSpacing(14)
        general_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        general_layout.setLabelAlignment(Qt.AlignRight)
        general_layout.setRowWrapPolicy(QFormLayout.DontWrapRows)

        section_title = QLabel("Download Settings")
        section_title.setStyleSheet("color: #1e293b; font-size: 11pt; font-weight: 600; margin-bottom: 2px;")
        general_layout.addRow(section_title)

        self.download_location = QLineEdit()
        self.download_location.setText(VSettings.get_download_location())
        browse_button = QPushButton("Browse...")
        browse_button.setMaximumWidth(90)
        browse_button.setFixedHeight(28)
        browse_button.clicked.connect(self.browse_download_location)

        download_layout = QHBoxLayout()
        download_layout.setSpacing(8)
        download_layout.addWidget(self.download_location)
        download_layout.addWidget(browse_button)

        general_layout.addRow("Download Location", download_layout)

        self.export_location = QLineEdit()
        self.export_location.setText(VSettings.get_export_location())
        export_browse_button = QPushButton("Browse...")
        export_browse_button.setMaximumWidth(90)
        export_browse_button.setFixedHeight(28)
        export_browse_button.clicked.connect(self.browse_export_location)

        export_layout = QHBoxLayout()
        export_layout.setSpacing(8)
        export_layout.addWidget(self.export_location)
        export_layout.addWidget(export_browse_button)

        general_layout.addRow("Export Links Location", export_layout)

        self.threads = QSpinBox()
        self.threads.setRange(1, 10)
        self.threads.setValue(VSettings.get_download_threads())

        self.retries = QSpinBox()
        self.retries.setRange(0, 10)
        self.retries.setValue(VSettings.get_download_retries())

        threads_layout = QHBoxLayout()
        threads_layout.setSpacing(12)
        threads_layout.addWidget(self.threads)
        threads_layout.addSpacing(16)
        threads_layout.addWidget(QLabel("Download Retries"))
        threads_layout.addWidget(self.retries)
        threads_layout.addStretch()

        general_layout.addRow("Download Threads", threads_layout)

        self.quality = QComboBox()
        self.quality.addItem("Best Quality", VideoQuality.BEST.value)
        self.quality.addItem("4K (2160p)", VideoQuality.P2160.value)
        self.quality.addItem("2K (1440p)", VideoQuality.P1440.value)
        self.quality.addItem("1080p (Full HD)", VideoQuality.P1080.value)
        self.quality.addItem("720p (HD)", VideoQuality.P720.value)
        self.quality.addItem("480p", VideoQuality.P480.value)
        self.quality.addItem("360p", VideoQuality.P360.value)
        self.quality.addItem("240p", VideoQuality.P240.value)
        self.quality.addItem("144p", VideoQuality.P144.value)
        self.quality.addItem("Audio Only", VideoQuality.AUDIO_ONLY.value)

        index = self.quality.findData(VSettings.get_download_quality())
        if index >= 0:
            self.quality.setCurrentIndex(index)

        general_layout.addRow("Video Quality", self.quality)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Plain)
        general_layout.addRow(separator)

        file_title = QLabel("File Settings")
        file_title.setStyleSheet(
            "color: #1e293b; font-size: 11pt; font-weight: 600; margin-top: 8px; margin-bottom: 2px;"
        )
        general_layout.addRow(file_title)

        self.caption_setting = QComboBox()
        self.caption_setting.addItem("Use video title", FileName.CAPTION)
        self.caption_setting.addItem("Use video ID", FileName.VIDEO_ID)
        self.caption_setting.addItem("Use random name", FileName.RANDOM)

        index = self.caption_setting.findData(VSettings.get_file_naming_mode())
        if index >= 0:
            self.caption_setting.setCurrentIndex(index)

        general_layout.addRow("File Naming", self.caption_setting)

        self.output_format = QComboBox()
        self.output_format.addItem("MP4 (.mp4)", OutputFormat.MP4.value)
        self.output_format.addItem("MKV (.mkv)", OutputFormat.MKV.value)
        self.output_format.addItem("WebM (.webm)", OutputFormat.WEBM.value)

        index = self.output_format.findData(VSettings.get_output_format())
        if index >= 0:
            self.output_format.setCurrentIndex(index)

        general_layout.addRow("Output Format", self.output_format)

        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine)
        separator2.setFrameShadow(QFrame.Plain)
        general_layout.addRow(separator2)

        organization_title = QLabel("Organization Settings")
        organization_title.setStyleSheet(
            "color: #1e293b; font-size: 11pt; font-weight: 600; margin-top: 8px; margin-bottom: 2px;"
        )
        general_layout.addRow(organization_title)

        self.playlist_org = QComboBox()
        self.playlist_org.addItem("Group by Playlist Name", PlaylistOrganization.BY_PLAYLIST)
        self.playlist_org.addItem("Group by Uploader", PlaylistOrganization.BY_UPLOADER)
        index = self.playlist_org.findData(VSettings.get_playlist_organization())
        if index >= 0:
            self.playlist_org.setCurrentIndex(index)
        general_layout.addRow("Playlist Organization", self.playlist_org)

        self.single_video_org = QComboBox()
        self.single_video_org.addItem("Group in Singles Folder", SingleVideoOrganization.GROUP_SINGLES)
        self.single_video_org.addItem("Group by Uploader", SingleVideoOrganization.BY_UPLOADER)
        index = self.single_video_org.findData(VSettings.get_single_video_organization())
        if index >= 0:
            self.single_video_org.setCurrentIndex(index)
        general_layout.addRow("Single Video Organization", self.single_video_org)

        advanced_tab = QWidget()
        advanced_layout = QFormLayout(advanced_tab)
        advanced_layout.setContentsMargins(18, 18, 18, 18)
        advanced_layout.setSpacing(14)
        advanced_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        advanced_layout.setLabelAlignment(Qt.AlignRight)
        advanced_layout.setRowWrapPolicy(QFormLayout.DontWrapRows)

        section_title = QLabel("Advanced Settings")
        section_title.setStyleSheet("color: #1e293b; font-size: 11pt; font-weight: 600; margin-bottom: 2px;")
        advanced_layout.addRow(section_title)

        self.cookies_browser_selector = QComboBox(self)
        self.cookies_browser_selector.addItems(
            ["None", "Chrome", "Firefox", "Edge", "Brave", "Opera", "Vivaldi", "Chromium"]
        )

        self.cookies_profile = QLineEdit()
        self.cookies_profile.setPlaceholderText("Profile name or path (optional)")

        self.cookies_profile_browse = QPushButton("Browse...")
        self.cookies_profile_browse.setMaximumWidth(90)
        self.cookies_profile_browse.setFixedHeight(28)
        self.cookies_profile_browse.clicked.connect(self.browse_cookies_profile)

        browser = VSettings.get_cookies_browser()
        profile = VSettings.get_cookies_profile()

        index = self.cookies_browser_selector.findText(browser.capitalize())
        self.cookies_browser_selector.setCurrentIndex(index if index >= 0 else 0)
        self.cookies_browser_selector.currentTextChanged.connect(self.update_cookies_browser)

        self.cookies_profile.setText(profile)
        self.update_cookies_browser()

        cookies_layout = QHBoxLayout()
        cookies_layout.setSpacing(8)
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
        self.back_button.setProperty("primary", "true")
        self.back_button.setMinimumWidth(130)
        self.back_button.setFixedHeight(32)
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
        VSettings.set_download_retries(self.retries.value())
        VSettings.set_download_quality(self.quality.currentData())
        VSettings.set_output_format(self.output_format.currentData())
        VSettings.set_playlist_organization(self.playlist_org.currentData())
        VSettings.set_single_video_organization(self.single_video_org.currentData())

        browser = self.cookies_browser_selector.currentText()
        VSettings.set_cookies_browser("" if browser == "None" else browser.lower())
        VSettings.set_cookies_profile("" if browser == "None" else self.cookies_profile.text().strip())

        super().accept()
