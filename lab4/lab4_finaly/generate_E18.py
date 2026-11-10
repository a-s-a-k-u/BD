import psycopg2
import random

configure = {
    "dbname": "lab4",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
}

def generate_audit_log():
    try:
        conn = psycopg2.connect(**configure)
        cursor = conn.cursor()

        actions = ["INSERT", "UPDATE", "STATUS_CHANGE", "SMEV_EXCHANGE"]
        entities = ["Пользователь", "Заявление", "Событие_статуса", "Межвед_запрос", "Начисление"]


        for i in range(1, 51):  #50 записей в журнале аудита
            event_date = f"2026-02-{(i % 28) + 1:02d} 20:{i % 60:02d}:00+03"
            action_type = random.choice(actions)
            entity_type = random.choice(entities)
            old_value = '{"Статус": "черновик"}' if action_type != "INSERT" else None
            new_value = f'{{"Статус": "обработано", "id": {i}}}'

            #id = i
            cursor.execute(
                """
                INSERT INTO Журнал_аудита (id, Дата_события, Тип_действия, Тип_сущности, Старое_значение, Новое_значение)
                VALUES (%s, %s, %s, %s, %s, %s);
                """,
                (i, event_date, action_type, entity_type, old_value, new_value)
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

generate_audit_log()
