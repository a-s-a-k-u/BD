import psycopg2
import random

configure = {
    "dbname": "lab4",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
}

def generate_regulation():
    try:
        conn = psycopg2.connect(**configure)
        cursor = conn.cursor()

        durations = [5, 10, 15, 30]
        statuses = ["действующий", "проект"]
        reg_counter = 1

        for service_id in range(1, 21):  #Для каждой из 20 услуг
            name = f"Административный регламент услуги №{service_id}"
            version = f"v1.{service_id}"
            approval_date = f"2025-01-{(service_id % 28) + 1:02d}"
            duration_days = random.choice(durations)
            expiry_date = "2027-12-31"
            status = random.choice(statuses)

            #id = reg_counter
            cursor.execute(
                """
                INSERT INTO Регламент (id, Наименование, Версия, Дата_утверждения, Срок_оказания_дней, Срок_действия, Статус, Услуга_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (reg_counter, name, version, approval_date, duration_days, expiry_date, status, service_id)
            )
            reg_counter += 1

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
    generate_regulation()
