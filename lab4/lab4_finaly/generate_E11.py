import psycopg2
import random

configure = {
    "dbname": "lab4",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
}

def generate_interdept_request():
    try:
        conn = psycopg2.connect(**configure)
        cursor = conn.cursor()

        statuses = ["отправлен", "доставлен", "исполнен"]

        for i in range(1, 26):  # 25 межведомственных запросов СМЭВ
            status = random.choice(statuses)
            request_number = f"SMEV-2026-{i:05d}"
            sent_at = f"2026-02-{(i % 28) + 1:02d} 12:15:00+03"
            content = f"Межведомственный запрос СМЭВ №{i} для проверки сведений заявителя"
            application_id = i
            initiator_dept_id = ((i - 1) % 5) + 1      #Ведомства 1..5
            receiver_dept_id = ((i - 1) % 5) + 6       #Ведомства 6..10 Иниц!=Пол

            # Явно передаем id = i
            cursor.execute(
                """
                INSERT INTO Межвед_запрос (id, Статус, Номер, Дата_отправки, Содержание, Заявление_id, Ведомство_инициатор_id, Ведомство_получатель_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (i, status, request_number, sent_at, content, application_id, initiator_dept_id, receiver_dept_id)
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

generate_interdept_request()
