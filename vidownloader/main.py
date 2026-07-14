import sys

from PyQt5.QtWidgets import QApplication

from vidownloader.core.Constants import App, Author, Paths
from vidownloader.core.Utils import exception_hook, load_fonts
from vidownloader.ui import stylesheets
from vidownloader.window.HomeWindow import HomeWindow


def main():
    Paths.ensure_paths()
    app = QApplication(sys.argv)

    app.setApplicationName(App.NAME)
    app.setOrganizationName(Author.NAME)
    app.setOrganizationDomain(Author.GITHUB)
    app.setStyleSheet(stylesheets.global_qss)

    sys.excepthook = exception_hook
    load_fonts()

    app.home_window = HomeWindow()
    app.home_window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
