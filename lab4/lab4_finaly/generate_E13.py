import psycopg2
import random

configure = {
    "dbname": "lab4",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
}

def generate_accrual():
    try:
        conn = psycopg2.connect(**configure)
        cursor = conn.cursor()

        amounts = [500.00, 1500.00, 2000.00, 4000.00, 6000.00]
        statuses = ["выставлено", "оплачено", "частично_оплачено"]

        for i in range(1, 31):
            currency = "RUB"
            basis = f"Госпошлина по заявлению №{i} (УИН 188100772026{i:04d})"
            amount = random.choice(amounts)
            accrual_date = f"2026-02-{(i % 28) + 1:02d}"
            status = random.choice(statuses)
            application_id = i
            department_id = ((i - 1) % 10) + 1

            cursor.execute(
                """
                INSERT INTO Начисление (id, Валюта, Основание, Сумма, Дата_начисления, Статус, Заявление_id, Ведомство_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (i, currency, basis, amount, accrual_date, status, application_id, department_id)
            )

        conn.commit()

    except Exception as e:
        print(f"Error in E13 -> {e}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    generate_accrual()