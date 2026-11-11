import psycopg2
import random

configure = {
    "dbname": "lab4",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
}

def generate_department():
    try:
        conn = psycopg2.connect(**configure)
        cursor = conn.cursor()

        dept_names = [
            "МВД России (ГУВМ)",
            "ФНС России",
            "Росреестр",
            "Социальный фонд России (СФР)",
            "Минцифры России",
            "Роспотребнадзор",
            "Минстрой России",
            "ФССП России",
            "Росимущество",
            "Минздрав России"
        ]

        dept_ids = []
        for i in range(1, 11):  #10 ведомств
            name = dept_names[i - 1]
            code = f"DEPT-{i:03d}"
            address = f"г. Москва, Правительственный пер., д. {i}"
            phone = f"+7499{6700000 + i:07d}"
            email = f"dept_{i}@gov.ru"

            #id = i
            cursor.execute(
                """
                INSERT INTO Ведомство (id, Наименование, Код, Адрес, Телефон, Электронная_почта)
                VALUES (%s, %s, %s, %s, %s, %s);
                """,
                (i, name, code, address, phone, email)
            )
            dept_ids.append(i)

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
    generate_department()