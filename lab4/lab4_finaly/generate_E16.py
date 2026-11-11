import psycopg2
import random

configure = {
    "dbname": "lab4",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
}

def generate_complaint():
    try:
        conn = psycopg2.connect(**configure)
        cursor = conn.cursor()

        types = ["Нарушение сроков", "Неправомерный отказ", "Требование лишних документов", "Технический сбой"]
        statuses = ["зарегистрирована", "на_рассмотрении", "удовлетворена", "отклонена"]

        for i in range(1, 16):
            complaint_number = f"CMP-2026-{i:04d}"
            submitted_at = f"2026-02-{(i % 28) + 1:02d} 17:00:00+03"
            content = f"Досудебная жалоба №{i} на нарушение регламента предоставления услуги"
            complaint_type = random.choice(types)
            status = random.choice(statuses)
            user_id = ((i - 1) % 50) + 1
            department_id = ((i - 1) % 10) + 1
            application_id = i

            cursor.execute(
                """
                INSERT INTO Жалоба (id, Номер, Дата_и_время_подачи, Содержание, Тип, Статус, Пользователь_id, Ведомство_id, Заявление_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (i, complaint_number, submitted_at, content, complaint_type, status, user_id, department_id, application_id)
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

if __name__ == "__main__":
    generate_complaint()