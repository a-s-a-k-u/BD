import psycopg2
import random

configure = {
    "dbname": "lab4",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
}

def generate_accrual_payment():
    try:
        conn = psycopg2.connect(**configure)
        cursor = conn.cursor()


        amounts = [500.00, 1500.00, 2000.00]

        for i in range(1, 31):  # связь E13 - E14
            accrual_id = i
            payment_id = i
            paid_amount = random.choice(amounts)
            paid_at = f"2026-02-{(i % 28) + 1:02d} 16:21:00+03"
            is_closing = (i % 3 != 0)

            # PK (Начисление_id, Платёж_id)
            cursor.execute(
                """
                INSERT INTO Оплата_начисления (Начисление_id, Платёж_id, Сумма_оплаты, Дата_оплаты, Признак_закрытия)
                VALUES (%s, %s, %s, %s, %s);
                """,
                (accrual_id, payment_id, paid_amount, paid_at, is_closing)
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

generate_accrual_payment()
