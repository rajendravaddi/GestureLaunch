import sys

from PySide6.QtWidgets import QApplication

from app.main_window import MainWindow



def main() -> None:
    application = QApplication(sys.argv)


    main_window = MainWindow()
    main_window.show()

    application.exec()


if __name__ == "__main__":
    main()