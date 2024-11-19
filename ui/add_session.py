from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton,QMessageBox

class AddSessionDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db

        self.setWindowTitle("Добавить сеанс")
        self.setGeometry(100, 100, 300, 200)

        self.layout = QVBoxLayout(self)
        self.movie_input = QLineEdit(self)
        self.movie_input.setPlaceholderText("Название фильма")
        self.layout.addWidget(self.movie_input)

        self.time_input = QLineEdit(self)
        self.time_input.setPlaceholderText("Время сеанса")
        self.layout.addWidget(self.time_input)

        self.seats_input = QLineEdit(self)
        self.seats_input.setPlaceholderText("Количество мест")
        self.layout.addWidget(self.seats_input)

        self.add_button = QPushButton("Добавить", self)
        self.add_button.clicked.connect(self.add_session)
        self.layout.addWidget(self.add_button)

    def add_session(self):
        movie = self.movie_input.text()
        time = self.time_input.text()
        try:
            seats = int(self.seats_input.text())
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Количество мест должно быть числом.")
            return

        # Добавляем сеанс в базу данных
        session_data = {"movie": movie, "time": time, "seats": seats}
        session_id = self.db.add_session(session_data)
        
        if session_id:
            QMessageBox.information(self, "Успех", "Сеанс добавлен.")
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось добавить сеанс.")
