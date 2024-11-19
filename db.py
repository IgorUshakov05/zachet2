from pymongo import MongoClient
from bson import ObjectId

from bson import ObjectId

class Database:
    def __init__(self, uri="mongodb://localhost:27017", db_name="booking_system"):
        # Подключение к базе данных
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.sessions = self.db["sessions"]

    def get_sessions(self):
        """Возвращает все сеансы"""
        return list(self.sessions.find())

    def get_session(self, session_id):
        """Возвращает конкретный сеанс по ID"""
        return self.sessions.find_one({"_id": ObjectId(session_id)})

    def update_seats(self, session_id, change):
        """Обновляет количество мест в сеансе"""
        self.sessions.update_one({"_id": ObjectId(session_id)}, {"$inc": {"seats": change}})

    def add_session(self, session_data):
        """Добавляет новый сеанс в коллекцию"""
        # Добавляем новый сеанс в коллекцию "sessions"
        result = self.sessions.insert_one(session_data)
        return result.inserted_id  # Возвращаем ID нового сеанса