# Система бронирования мест

## Описание

Система бронирования мест для сеансов в кинотеатре. Проект реализован с использованием **PySide6** для создания графического интерфейса пользователя и **MongoDB** для хранения данных.

### Основные возможности:
- Добавление сеансов (фильм, время сеанса, количество доступных мест).
- Бронирование мест для сеансов.
- Отмена бронирования.
- Отображение сеансов в таблице.

## Установка и запуск

Для того чтобы запустить проект, выполните следующие шаги:

1. Клонируйте репозиторий на ваш локальный компьютер.
   ```bash
   git clone https://github.com/your-repo/booking-system.git
Установите необходимые зависимости:

pip install -r requirements.txt
Убедитесь, что у вас установлен MongoDB и сервер запущен на localhost:27017.

Запустите приложение:

python main.py
Структура проекта
├── db.py                # Логика работы с базой данных
├── main.py              # Главный скрипт запуска
├── ui/                  # Папка с интерфейсами
│   ├── main_window.py   # Главное окно приложения
│   ├── add_session.py   # Диалоговое окно для добавления сеанса
│   └── booking_form.py  # Диалоговое окно для бронирования мест
└── requirements.txt     # Список зависимостей
Описание кода
db.py — Работа с базой данных
Класс Database отвечает за взаимодействие с MongoDB. В нем реализованы методы для получения, добавления и обновления сеансов.

```python
from pymongo import MongoClient
from bson import ObjectId

class Database:
    def __init__(self, uri="mongodb://localhost:27017", db_name="booking_system"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.sessions = self.db["sessions"]
        self.bookings = self.db["bookings"]

    def get_sessions(self):
        """Возвращает все сеансы из базы данных."""
        return list(self.sessions.find())

    def get_session(self, session_id):
        """Возвращает конкретный сеанс по ID."""
        return self.sessions.find_one({"_id": ObjectId(session_id)})

    def add_session(self, session_data):
        """Добавляет новый сеанс в коллекцию sessions."""
        result = self.sessions.insert_one(session_data)
        return result.inserted_id

    def update_seats(self, session_id, change):
        """Обновляет количество мест в сеансе."""
        self.sessions.update_one({"_id": ObjectId(session_id)}, {"$inc": {"seats": change}})
        ```
Описание методов:
get_sessions(): Получение списка всех сеансов.
get_session(session_id): Получение информации о конкретном сеансе по ID.
add_session(session_data): Добавление нового сеанса в базу данных.
update_seats(session_id, change): Обновление количества мест для указанного сеанса.
ui/main_window.py — Главное окно приложения
Этот файл создает главное окно приложения с меню и таблицей, где отображаются все сеансы. Также есть возможность добавить новый сеанс через диалоговое окно.

```python
from PySide6.QtWidgets import QMainWindow, QTableWidget, QVBoxLayout, QWidget, QAction, QTableWidgetItem
from ui.add_session import AddSessionDialog
from db import Database

class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Система бронирования")

        # Меню для добавления сеансов
        menu_bar = self.menuBar()
        session_menu = menu_bar.addMenu("Сеансы")
        add_session_action = QAction("Добавить сеанс", self)
        add_session_action.triggered.connect(self.add_session)
        session_menu.addAction(add_session_action)

        self.table = self.init_table()
        self.refresh_table()

    def init_table(self):
        """Инициализирует таблицу для отображения сеансов."""
        table = QTableWidget(self)
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["ID", "Фильм", "Время"])
        return table

    def refresh_table(self):
        """Обновляет таблицу с сеансами из базы данных."""
        self.table.setRowCount(0)
        sessions = self.db.get_sessions()
        for row_idx, session in enumerate(sessions):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(session["_id"])))
            self.table.setItem(row_idx, 1, QTableWidgetItem(session["movie"]))
            self.table.setItem(row_idx, 2, QTableWidgetItem(session["time"]))

    def add_session(self):
        """Открывает окно для добавления нового сеанса."""
        dialog = AddSessionDialog(self.db, self)
        if dialog.exec():
            self.refresh_table()
            ```
Описание методов:
init_table(): Инициализация таблицы для отображения сеансов.
refresh_table(): Обновление содержимого таблицы с сеансами.
add_session(): Открытие диалогового окна для добавления нового сеанса.
ui/add_session.py — Диалоговое окно для добавления сеанса
Этот файл реализует диалоговое окно для ввода информации о новом сеансе: название фильма, время и количество мест.

```python
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
from db import Database

class AddSessionDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Добавить сеанс")

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
        """Добавляет новый сеанс в базу данных."""
        movie = self.movie_input.text()
        time = self.time_input.text()
        try:
            seats = int(self.seats_input.text())
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Количество мест должно быть числом.")
            return

        # Добавление сеанса в базу данных
        session_data = {"movie": movie, "time": time, "seats": seats}
        session_id = self.db.add_session(session_data)
        
        if session_id:
            QMessageBox.information(self, "Успех", "Сеанс добавлен.")
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось добавить сеанс.")
            ```
Описание методов:
add_session(): Добавление нового сеанса в базу данных.
ui/booking_form.py — Диалоговое окно для бронирования мест
Этот файл управляет процессом бронирования мест. Пользователь выбирает сеанс и бронирует места.

```python
from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox

class BookingForm(QDialog):
    def __init__(self, db, session_id, parent=None):
        super().__init__(parent)
        self.db = db
        self.session_id = session_id

        self.setWindowTitle("Бронирование мест")

        # Таблица для отображения информации о сеансе
        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Фильм", "Время"])
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.table)

        self.book_button = QPushButton("Забронировать место", self)
        self.book_button.clicked.connect(self.book_seat)
        self.layout.addWidget(self.book_button)

        self.load_session_info()

    def load_session_info(self):
        """Загружает информацию о сеансе для отображения."""
        session = self.db.get_session(self.session_id)
        if session:
            self.table.setRowCount(1)
            self.table.setItem(0, 0, QTableWidgetItem(str(session["_id"])))
            self.table.setItem(0, 1, QTableWidgetItem(session["movie"]))
            self.table.setItem(0, 2, QTableWidgetItem(session["time"]))

    def book_seat(self):
        """Бронирует место на сеансе."""
        self.db.update_seats(self.session_id, -1)
        QMessageBox.information(self, "Успех", "Место забронировано!")
        self.accept()
```





