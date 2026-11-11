import psycopg2
import random

configure = {
    "dbname": "lab4",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
}

def generate_complaint_decision():
    try:
        conn = psycopg2.connect(**configure)
        cursor = conn.cursor()


        decision_types = ["удовлетворить_полностью", "удовлетворить_частично", "отказать"]


        for i in range(1, 16):
            decision_type = random.choice(decision_types)
            decision_text = f"Официальное решение комиссии ведомства по жалобе №{i}: {decision_type}"
            decided_at = f"2026-02-{(i % 28) + 1:02d} 19:00:00+03"
            user_id = ((i - 1) % 10) + 1
            complaint_id = i

            cursor.execute(
                """
                INSERT INTO Решение_по_жалобе (id, Вид_решения, Решение, Дата_и_время_решения, Пользователь_id, Жалоба_id)
                VALUES (%s, %s, %s, %s, %s, %s);
                """,
                (i, decision_type, decision_text, decided_at, user_id, complaint_id)
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
    generate_complaint_decision()