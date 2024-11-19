from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
from bson import ObjectId


class BookingForm(QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db

        self.layout = QVBoxLayout(self)
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID сеанса", "Фильм", "Время", "Свободные места"])
        self.layout.addWidget(self.table)

        # Кнопка для бронирования
        self.book_button = QPushButton("Забронировать место", self)
        self.book_button.clicked.connect(self.book_seat)
        self.layout.addWidget(self.book_button)

        # Кнопка для отмены бронирования
        self.cancel_button = QPushButton("Отменить бронирование", self)
        self.cancel_button.clicked.connect(self.cancel_booking)
        self.layout.addWidget(self.cancel_button)

        self.refresh_table()

    def refresh_table(self):
        self.table.setRowCount(0)
        sessions = self.db.get_sessions()
        for row_idx, session in enumerate(sessions):
            self.table.insertRow(row_idx)
            # Преобразуем ObjectId в строку для отображения
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(session["_id"])))
            self.table.setItem(row_idx, 1, QTableWidgetItem(session["movie"]))
            self.table.setItem(row_idx, 2, QTableWidgetItem(session["time"]))
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(session["seats"])))

    def book_seat(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите сеанс для бронирования.")
            return

        session_id_str = self.table.item(selected_row, 0).text()
        try:
            # Преобразуем строку обратно в ObjectId
            session_id = ObjectId(session_id_str)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Невозможно преобразовать ID сеанса: {e}")
            return

        session = self.db.get_session(session_id)
        if session and session.get("seats", 0) > 0:
            self.db.update_seats(session_id, -1)
            QMessageBox.information(self, "Успех", "Место забронировано.")
        else:
            QMessageBox.warning(self, "Ошибка", "Нет свободных мест.")

        self.refresh_table()

    def cancel_booking(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите сеанс для отмены бронирования.")
            return

        session_id_str = self.table.item(selected_row, 0).text()
        try:
            # Преобразуем строку обратно в ObjectId
            session_id = ObjectId(session_id_str)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Невозможно преобразовать ID сеанса: {e}")
            return

        self.db.update_seats(session_id, 1)
        QMessageBox.information(self, "Успех", "Бронирование отменено.")
        self.refresh_table()
