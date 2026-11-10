import psycopg2
import random

configure = {
    "dbname": "lab4",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
}

def generate_organization():
    try:
        conn = psycopg2.connect(**configure)
        cursor = conn.cursor()

        prefixes = ["ООО", "АО", "ПАО"]
        streets = ["Ленинский пр-т", "Каширское ш.", "пр-т Мира", "ул. Профсоюзная", "Тверская ул."]

        org_ids = []
        for i in range(1, 21):  #20 организаций
            name = f"{random.choice(prefixes)} «ТехноПарк-{i}»"
            inn = f"{7701000000 + i:010d}"
            ogrn = f"{1027700000000 + i:013d}"
            address = f"г. Москва, {random.choice(streets)}, д. {i}"
            phone = f"+7495{1000000 + i:07d}"
            email = f"org_{i}@corp-portal.ru"

            #id = i
            cursor.execute(
                """
                INSERT INTO Организация_заявителя (id, Наименование, ИНН, ОГРН, Адрес, Телефон, Электронная_почта)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
                """,
                (i, name, inn, ogrn, address, phone, email)
            )
            org_ids.append(i)

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

generate_organization()
