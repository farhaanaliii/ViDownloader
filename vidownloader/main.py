import sys

from vidownloader.ui import stylesheets, resources_rc
from vidownloader.window.HomeWindow import HomeWindow
from vidownloader.core.Constants import App, Author, Paths
from vidownloader.core.Utils import load_fonts, exception_hook

from PyQt5.QtWidgets import QApplication


def main():
    Paths.ensure_paths()
    app = QApplication(sys.argv)
    
    app.setApplicationName(App.NAME)
    app.setOrganizationName(Author.NAME)
    app.setOrganizationDomain(Author.GITHUB)
    app.setStyleSheet(stylesheets.global_qss)
    
    sys.excepthook = exception_hook
    load_fonts()
    
    window = HomeWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
