import psycopg2
import random

configure = {
    "dbname": "lab4",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
}

def generate_user():
    try:
        conn = psycopg2.connect(**configure)
        cursor = conn.cursor()

        last_names = ["Иванов", "Петров", "Сидоров", "Смирнов", "Кузнецов", "Соколов", "Попов", "Морозов"]
        first_names = ["Алексей", "Дмитрий", "Иван", "Михаил", "Сергей", "Андрей", "Максим", "Артем"]
        middle_names = ["Сергеевич", "Александрович", "Викторович", "Игоревич", "Павлович", "Олегович"]
        roles = ["заявитель", "представитель_юрлица", "сотрудник_ведомства", "администратор"]

        for i in range(1, 51):  #50 пользователей
            last_name = random.choice(last_names)
            first_name = random.choice(first_names)
            middle_name = random.choice(middle_names)
            email = f"user_{i}@gosportal.ru"
            phone = f"+7916{2000000 + i:07d}"

            if i <= 10:
                role = "сотрудник_ведомства"
                org_id = None
            elif i <= 25:
                role = "представитель_юрлица"
                org_id = ((i - 1) % 20) + 1  #Ссылка на Организация_заявителя
            else:
                role = random.choice(roles)
                org_id = ((i - 1) % 20) + 1 if role == "представитель_юрлица" else None

            #id = i
            cursor.execute(
                """
                INSERT INTO Пользователь (id, Фамилия, Имя, Отчество, Электронная_почта, Телефон, Роль, Организация_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (i, last_name, first_name, middle_name, email, phone, role, org_id)
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
    generate_user()