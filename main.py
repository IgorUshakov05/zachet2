import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtGui import QIcon  # Импорт QIcon
from ui.main_window import MainWindow
from db import Database

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("resources/icon.png"))  # Установка иконки

    db = Database()  # Подключение к базе данных
    window = MainWindow(db)
    window.setWindowTitle("Система бронирования")
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
