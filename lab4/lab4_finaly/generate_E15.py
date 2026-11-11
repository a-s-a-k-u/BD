import psycopg2
import random

configure = {
    "dbname": "lab4",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
}

def generate_appointment():
    try:
        conn = psycopg2.connect(**configure)
        cursor = conn.cursor()
        for i in range(1, 21):  # 20 записей на личный прием в МФЦ/ведомство
            appointment_date = f"2026-03-{(i % 28) + 1:02d}"
            hour = 9 + (i % 8)
            start_time = f"{hour:02d}:00:00"
            end_time = f"{hour:02d}:30:00"
            address = f"г. Москва, Центр госуслуг «Мои Документы», окно №{(i % 15) + 1}"
            user_id = ((i - 1) % 50) + 1
            service_id = ((i - 1) % 20) + 1
            application_id = i  # AK1 на Заявление_id

            # id = i
            cursor.execute(
                """
                INSERT INTO Запись_на_приём (id, Дата_приема, Время_начала, Время_окончания, Адрес, Пользователь_id, Услуга_id, Заявление_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (i, appointment_date, start_time, end_time, address, user_id, service_id, application_id)
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

