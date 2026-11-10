import psycopg2
import random

configure = {
    "dbname": "lab4",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
}

def generate_document_version():
    try:
        conn = psycopg2.connect(**configure)
        cursor = conn.cursor()

        version_counter = 0
        for doc_id in range(1, 41):     #Для каждого из 40 документов
            for ver_num in range(1, 3): #2 версии на каждый документ
                content = f"Скан-копия документа #{doc_id}, ревизия v{ver_num}.0 (проверено УКЭП)"
                created_at = f"2026-02-{(doc_id % 28) + 1:02d} 11:{ver_num * 15:02d}:00+03"
                user_id = ((doc_id - 1) % 50) + 1

                # PK (id = ver_num, Документ_id = doc_id)
                cursor.execute(
                    """
                    INSERT INTO Версия_документа (id, Документ_id, Содержимое, Дата_создания, Пользователь_id)
                    VALUES (%s, %s, %s, %s, %s);
                    """,
                    (ver_num, doc_id, content, created_at, user_id)
                )
                version_counter += 1

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

generate_document_version()
