import psycopg2
import random

configure = {
    "dbname": "lab4",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
}

def generate_interdept_response():
    try:
        conn = psycopg2.connect(**configure)
        cursor = conn.cursor()

        statuses = ["получен", "принят"]

        for i in range(1, 26):  #По одному ответу на каждый из 25 запросов 1:1
            status = random.choice(statuses)
            responded_at = f"2026-02-{(i % 28) + 1:02d} 12:45:00+03"
            content = f"Официальный ответ СМЭВ на запрос №{i}: сведения подтверждены"
            request_id = i
            department_id = ((i - 1) % 5) + 6  #Ведомство-получатель, сформировавшее ответ

            #id = i
            cursor.execute(
                """
                INSERT INTO Ответ_на_запрос (id, Статус, Дата_ответа, Содержание, Запрос_id, Ведомство_id)
                VALUES (%s, %s, %s, %s, %s, %s);
                """,
                (i, status, responded_at, content, request_id, department_id)
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

generate_interdept_response()
