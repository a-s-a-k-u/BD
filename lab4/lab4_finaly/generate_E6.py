import psycopg2
import random

configure = {
    "dbname": "lab4",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
}

def generate_regulation_requirement():
    try:
        conn = psycopg2.connect(**configure)
        cursor = conn.cursor()

        total_reqs = 0
        for reg_id in range(1, 21):      #Для каждого из 20 регламентов
            for req_id in range(1, 4):   #По 3 требования внутри каждого регламента
                name = f"Требование п.{req_id} регламента №{reg_id}"
                description = f"Обязательное предоставление документа по пункту {req_id}"
                is_mandatory = (req_id <= 2)

                # Явно передаем составной ключ (id = req_id, Регламент_id = reg_id)
                cursor.execute(
                    """
                    INSERT INTO Требование_регламента (id, Регламент_id, Наименование, Описание, Обязательность)
                    VALUES (%s, %s, %s, %s, %s);
                    """,
                    (req_id, reg_id, name, description, is_mandatory)
                )
                total_reqs += 1

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
    generate_regulation_requirement()
