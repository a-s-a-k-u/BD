import psycopg2
import random

configure = {
    "dbname": "lab4",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
}

def generate_application():
    try:
        conn = psycopg2.connect(**configure)
        cursor = conn.cursor()

        statuses = ["зарегистрировано", "на_проверке", "ожидает_оплаты", "межвед_запрос", "исполнено", "отказано"]

        for i in range(1, 41):  # 40 заявлений
            app_number = f"APP-2026-{i:05d}"
            user_id = ((i - 1) % 50) + 1
            regulation_id = ((i - 1) % 20) + 1
            submitted_at = f"2026-02-{(i % 28) + 1:02d} 10:{i % 60:02d}:00+03"
            request_content = f"Запрос на предоставление государственной услуги по регламенту №{regulation_id}"
            status = random.choice(statuses)

            # id = i
            cursor.execute(
                """
                INSERT INTO Заявление (id, Номер, Пользователь_id, Регламент_id, Дата_подачи, Состав_запроса, Статус)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
                """,
                (i, app_number, user_id, regulation_id, submitted_at, request_content, status)
            )

        conn.commit()

    except Exception as e:
        print(f"Error -> {e}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

generate_application()
