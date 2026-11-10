import psycopg2
import random

configure = {
    "dbname": "lab4",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
}

def generate_payment():
    try:
        conn = psycopg2.connect(**configure)
        cursor = conn.cursor()

        amounts = [500.00, 1500.00, 2000.00, 4000.00, 6000.00]
        methods = ["сбп", "банковская_карта", "лицевой_счет", "квитанция"]

        for i in range(1, 31):  #30 платежей
            status = "проведен"
            currency = "RUB"
            amount = random.choice(amounts)
            payment_date = f"2026-02-{(i % 28) + 1:02d} 16:20:00+03"
            payment_method = random.choice(methods)
            user_id = ((i - 1) % 50) + 1

            # Явно передаем id = i
            cursor.execute(
                """
                INSERT INTO Платеж (id, Статус, Валюта, Сумма, Дата_платежа, Способ_оплаты, Пользователь_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
                """,
                (i, status, currency, amount, payment_date, payment_method, user_id)
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

generate_payment()
