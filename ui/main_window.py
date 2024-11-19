from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QMainWindow, QTableWidget, QTableWidgetItem, QTabWidget, QWidget, QVBoxLayout, QMessageBox
)
from ui.add_session import AddSessionDialog
from ui.booking_form import BookingForm


class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Система бронирования")

        # Добавляем меню
        menu_bar = self.menuBar()
        session_menu = menu_bar.addMenu("Сеансы")
        add_session_action = QAction("Добавить сеанс", self)
        add_session_action.triggered.connect(self.add_session)
        session_menu.addAction(add_session_action)

        # Основной виджет с вкладками
        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)

        # Вкладка для сеансов
        self.session_tab = QWidget()
        self.session_layout = QVBoxLayout(self.session_tab)
        self.table = self.init_table()
        self.session_layout.addWidget(self.table)
        self.tabs.addTab(self.session_tab, "Сеансы")

        # Вкладка для бронирования
        self.booking_tab = BookingForm(self.db, self)
        self.tabs.addTab(self.booking_tab, "Бронирование")

        self.refresh_table()

    def init_table(self):
        table = QTableWidget(self)
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["ID", "Фильм", "Время"])
        return table

    def refresh_table(self):
        self.table.setRowCount(0)
        sessions = self.db.get_sessions()
        for row_idx, session in enumerate(sessions):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(session["_id"])))
            self.table.setItem(row_idx, 1, QTableWidgetItem(session["movie"]))
            self.table.setItem(row_idx, 2, QTableWidgetItem(session["time"]))

    def add_session(self):
        dialog = AddSessionDialog(self.db, self)
        if dialog.exec():
            QMessageBox.information(self, "Успех", "Сеанс добавлен.")
            self.refresh_table()
