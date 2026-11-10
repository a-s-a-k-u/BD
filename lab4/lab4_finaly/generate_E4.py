import psycopg2
import random

configure = {
    "dbname": "lab4",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
}

def generate_service():
    try:
        conn = psycopg2.connect(**configure)
        cursor = conn.cursor()

        costs = [500.00, 1500.00, 2000.00, 4000.00, 6000.00]
        service_counter = 1

        for dept_id in range(1, 11):  #Для каждого из 10 ведомств
            for j in range(1, 3):     #По 2 услуги на каждое ведомство 2 * 10
                name = f"Государственная услуга №{service_counter} (Ведомство {dept_id})"
                description = f"Официальное предоставление госуслуги #{service_counter}"
                is_paid = (service_counter % 2 == 1)
                cost = random.choice(costs) if is_paid else 0.00

                #id = service_counter
                cursor.execute(
                    """
                    INSERT INTO Услуга (id, Наименование, Описание, Стоимость, Признак_платности, Ведомство_id)
                    VALUES (%s, %s, %s, %s, %s, %s);
                    """,
                    (service_counter, name, description, cost, is_paid, dept_id)
                )
                service_counter += 1

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

generate_service()
