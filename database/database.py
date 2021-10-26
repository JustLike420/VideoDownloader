import psycopg2
from config import db
from contextlib import closing


class Database(object):

    def connect(self):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = psycopg2.connect(database=db.database, user=db.user,
                                           password=db.password, host=db.host)
        return self.connection

    def get_users(self, status="true"):
        """Получаем всех активных подписчиков бота"""
        with closing(self.connect()) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE status = %s", (status,))
                return cursor.fetchall()

    def subscriber_exists(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            self.cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            return bool(len(self.cursor.fetchall()))

    def add_subscriber(self, user_id, status="true"):
        """Добавляем нового подписчика"""
        with self.connection:
            self.cursor.execute("INSERT INTO users (user_id, status) VALUES(%s, %s)", (user_id, status))

    def update_subscription(self, user_id, status):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            self.cursor.execute("UPDATE users SET status = %s WHERE user_id = %s", (status, user_id))

    def get_words(self, user_id, status="true"):
        """Получить все ключевые слова"""
        with self.connection:
            self.cursor.execute("SELECT words FROM users WHERE user_id = %s AND status = %s", (user_id, status))
            result = self.cursor.fetchone()
            return result or "x100"

    def add_words(self, user_id, message, status="true"):
        """Добавляем слова для поиска на бирже"""
        with self.connection:
            self.cursor.execute("UPDATE users SET words = %s WHERE user_id = %s AND status = %s",
                                (message, user_id, status))
            rowcount = self.cursor.rowcount
        return rowcount if rowcount > 0 else "x100"

    def get_project_info(self, link):
        """Получаем полную информацию о проекте"""
        with self.connection:
            self.cursor.execute("SELECT * FROM projects_info WHERE link = %s", (link,))
            result = self.cursor.fetchone()
            return result or "x001"

    def add_projects(self, projects):
        """Сохранение информации о биржах"""
        with self.connection:
            for project in projects:
                self.cursor.execute(
                    "INSERT INTO projects_info (title, link, description, full_description) VALUES (%s,%s,%s,%s)",
                    (project["title"], project["link"], project["description"], project["full_description"]))

    # def close(self):
    #     """Закрываем соединение с БД"""
    #     self.connection.close()
