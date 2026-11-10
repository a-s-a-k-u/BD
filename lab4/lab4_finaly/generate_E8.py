import psycopg2
import random

configure = {
    "dbname": "lab4",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
}

def generate_application_document():
    try:
        conn = psycopg2.connect(**configure)
        cursor = conn.cursor()
        doc_types = ["Паспорт РФ", "Доверенность", "Выписка ЕГРН", "Справка о доходах", "Устав организации"]
        doc_counter = 1

        for app_id in range(1, 41):  #По 1 документу на каждое из 40 заявлений
            issue_date = f"2021-05-{(app_id % 28) + 1:02d}"
            doc_type = random.choice(doc_types)
            name = f"{doc_type} (к заявлению №{app_id})"

            # id = doc_counter
            # Заявление_id = app_id
            cursor.execute(
                """
                INSERT INTO Документ_заявления (id, Заявление_id, Дата_выдачи, Наименование, Тип)
                VALUES (%s, %s, %s, %s, %s);
                """,
                (doc_counter, app_id, issue_date, name, doc_type)
            )
            doc_counter += 1

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

generate_application_document()
