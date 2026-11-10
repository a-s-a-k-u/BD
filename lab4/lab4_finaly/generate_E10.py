import psycopg2
import random

configure = {
    "dbname": "lab4",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
}

def generate_status_event():
    try:
        conn = psycopg2.connect(**configure)
        cursor = conn.cursor()

        next_statuses = ["на_проверке", "межвед_запрос", "ожидает_оплаты", "исполнено"]
        event_counter = 1

        for app_id in range(1, 41):  #Для каждого из 40 заявлений создаем 2 события перехода статуса
            dept_id = ((app_id - 1) % 10) + 1
            staff_user_id = ((app_id - 1) % 10) + 1

            #1-е событие: регистрация заявления
            cursor.execute(
                """
                INSERT INTO Событие_статуса (id, Статус_из, Статус_в, Дата_события, Срок_исполнения, Заявление_id, Ведомство_id, Пользователь_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (event_counter, "черновик", "зарегистрировано", f"2026-02-{(app_id % 28) + 1:02d} 10:05:00+03", "2026-03-01", app_id, dept_id, staff_user_id)
            )
            event_counter += 1

            #2-е событие: переход в рабочий статус
            cursor.execute(
                """
                INSERT INTO Событие_статуса (id, Статус_из, Статус_в, Дата_события, Срок_исполнения, Заявление_id, Ведомство_id, Пользователь_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (event_counter, "зарегистрировано", random.choice(next_statuses), f"2026-02-{(app_id % 28) + 1:02d} 14:30:00+03", "2026-03-10", app_id, dept_id, staff_user_id)
            )
            event_counter += 1

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

generate_status_event()
