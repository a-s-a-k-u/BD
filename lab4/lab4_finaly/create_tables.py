import psycopg2

configure = {
    "dbname": "lab4",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
}

def create_tables():
    try:
        conn = psycopg2.connect(**configure)
        cursor = conn.cursor()

        cursor.execute("""
        DROP TABLE IF EXISTS
            Журнал_аудита,
            Решение_по_жалобе,
            Жалоба,
            Запись_на_приём,
            Оплата_начисления,
            Платеж,
            Начисление,
            Ответ_на_запрос,
            Межвед_запрос,
            Событие_статуса,
            Версия_документа,
            Документ_заявления,
            Заявление,
            Требование_регламента,
            Регламент,
            Услуга,
            Ведомство,
            Пользователь,
            Организация_заявителя
        CASCADE;
        """)

        #E2-Организация заявителя
        cursor.execute("""
        CREATE TABLE Организация_заявителя (
            id BIGINT PRIMARY KEY,
            Наименование VARCHAR(255) NOT NULL,
            ИНН VARCHAR(12) NOT NULL UNIQUE,
            ОГРН VARCHAR(15) NOT NULL UNIQUE,
            Адрес TEXT NOT NULL,
            Телефон VARCHAR(20) NOT NULL,
            Электронная_почта VARCHAR(255) NOT NULL UNIQUE
        );
        """)

        #E1-Пользователь
        cursor.execute("""
        CREATE TABLE Пользователь (
            id BIGINT PRIMARY KEY,
            Фамилия VARCHAR(100) NOT NULL,
            Имя VARCHAR(100) NOT NULL,
            Отчество VARCHAR(100),
            Электронная_почта VARCHAR(255) NOT NULL UNIQUE,
            Телефон VARCHAR(20) NOT NULL UNIQUE,
            Роль VARCHAR(30) NOT NULL,
            Организация_id BIGINT REFERENCES Организация_заявителя(id) ON DELETE SET NULL ON UPDATE CASCADE
        );
        """)

        #E3-Ведомство
        cursor.execute("""
        CREATE TABLE Ведомство (
            id BIGINT PRIMARY KEY,
            Наименование VARCHAR(255) NOT NULL,
            Код VARCHAR(50) NOT NULL UNIQUE,
            Адрес TEXT NOT NULL,
            Телефон VARCHAR(20) NOT NULL,
            Электронная_почта VARCHAR(255) NOT NULL UNIQUE
        );
        """)

        #E4-Услуга
        cursor.execute("""
        CREATE TABLE Услуга (
            id BIGINT PRIMARY KEY,
            Наименование VARCHAR(255) NOT NULL,
            Описание TEXT,
            Стоимость NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
            Признак_платности BOOLEAN NOT NULL DEFAULT FALSE,
            Ведомство_id BIGINT NOT NULL REFERENCES Ведомство(id) ON DELETE RESTRICT ON UPDATE CASCADE
        );
        """)
        #E5-Регламент
        cursor.execute("""
        CREATE TABLE Регламент (
            id BIGINT PRIMARY KEY,
            Наименование VARCHAR(255) NOT NULL,
            Версия VARCHAR(20) NOT NULL,
            Дата_утверждения DATE NOT NULL,
            Срок_оказания_дней INTEGER NOT NULL,
            Срок_действия DATE,
            Статус VARCHAR(20) NOT NULL,
            Услуга_id BIGINT NOT NULL REFERENCES Услуга(id) ON DELETE RESTRICT ON UPDATE CASCADE,
            UNIQUE (Версия, Услуга_id) 
        );
        """)
        #E6-Требование регламента
        cursor.execute("""
        CREATE TABLE Требование_регламента (
            id INTEGER NOT NULL,
            Регламент_id BIGINT NOT NULL REFERENCES Регламент(id) ON DELETE CASCADE ON UPDATE CASCADE,
            Наименование VARCHAR(255) NOT NULL,
            Описание TEXT NOT NULL,
            Обязательность BOOLEAN NOT NULL DEFAULT TRUE,
            PRIMARY KEY (id, Регламент_id)
        );
        """)

        #E7-Заявление
        cursor.execute("""
        CREATE TABLE Заявление (
            id BIGINT PRIMARY KEY,
            Номер VARCHAR(50) NOT NULL UNIQUE,
            Пользователь_id BIGINT NOT NULL REFERENCES Пользователь(id) ON DELETE RESTRICT ON UPDATE CASCADE,
            Регламент_id BIGINT NOT NULL REFERENCES Регламент(id) ON DELETE RESTRICT ON UPDATE CASCADE,
            Дата_и_время_подачи TIMESTAMPTZ NOT NULL,
            Состав_запроса TEXT NOT NULL,
            Статус VARCHAR(30) NOT NULL
        );
        """)

        #E8-Документ заявления
        cursor.execute("""
        CREATE TABLE Документ_заявления (
            id BIGINT NOT NULL UNIQUE,
            Заявление_id BIGINT NOT NULL REFERENCES Заявление(id) ON DELETE CASCADE ON UPDATE CASCADE,
            Дата_выдачи DATE NOT NULL,
            Наименование VARCHAR(255) NOT NULL,
            Тип VARCHAR(50) NOT NULL,
            PRIMARY KEY (id, Заявление_id)
        );
        """)

        #E9-Версия документа
        cursor.execute("""
        CREATE TABLE Версия_документа (
            id INTEGER NOT NULL,
            Документ_id BIGINT NOT NULL REFERENCES Документ_заявления(id) ON DELETE CASCADE ON UPDATE CASCADE,
            Содержимое TEXT NOT NULL,
            Дата_и_время_создания TIMESTAMPTZ NOT NULL,
            Пользователь_id BIGINT NOT NULL REFERENCES Пользователь(id) ON DELETE RESTRICT ON UPDATE CASCADE,
            PRIMARY KEY (id, Документ_id)
        );
        """)

        # E10-Событие статуса
        cursor.execute("""
        CREATE TABLE Событие_статуса (
            id BIGINT PRIMARY KEY,
            Статус_из VARCHAR(30),
            Статус_в VARCHAR(30) NOT NULL,
            Дата_и_время_события TIMESTAMPTZ NOT NULL,
            Срок_исполнения DATE,
            Заявление_id BIGINT NOT NULL REFERENCES Заявление(id) ON DELETE CASCADE ON UPDATE CASCADE,
            Ведомство_id BIGINT NOT NULL REFERENCES Ведомство(id) ON DELETE RESTRICT ON UPDATE CASCADE,
            Пользователь_id BIGINT NOT NULL REFERENCES Пользователь(id) ON DELETE RESTRICT ON UPDATE CASCADE
        );
        """)

        # E11- Межвед запрос
        cursor.execute("""
        CREATE TABLE Межвед_запрос (
            id BIGINT PRIMARY KEY,
            Статус VARCHAR(20) NOT NULL,
            Номер VARCHAR(50) NOT NULL UNIQUE,
            Дата_и_время_отправки TIMESTAMPTZ NOT NULL,
            Содержание TEXT NOT NULL,
            Заявление_id BIGINT NOT NULL REFERENCES Заявление(id) ON DELETE RESTRICT ON UPDATE CASCADE,
            Ведомство_инициатор_id BIGINT NOT NULL REFERENCES Ведомство(id) ON DELETE RESTRICT ON UPDATE CASCADE,
            Ведомство_получатель_id BIGINT NOT NULL REFERENCES Ведомство(id) ON DELETE RESTRICT ON UPDATE CASCADE,
            CHECK (Ведомство_инициатор_id <> Ведомство_получатель_id)
        );
        """)

        #E12-Ответ на запрос
        cursor.execute("""
        CREATE TABLE Ответ_на_запрос (
            id BIGINT PRIMARY KEY,
            Статус VARCHAR(20) NOT NULL,
            Дата_и_время_ответа TIMESTAMPTZ NOT NULL,
            Содержание TEXT NOT NULL,
            Запрос_id BIGINT NOT NULL UNIQUE REFERENCES Межвед_запрос(id) ON DELETE CASCADE ON UPDATE CASCADE,
            Ведомство_id BIGINT NOT NULL REFERENCES Ведомство(id) ON DELETE RESTRICT ON UPDATE CASCADE
        );
        """)

        #E13-Начисление
        cursor.execute("""
        CREATE TABLE Начисление (
            id BIGINT PRIMARY KEY,
            Валюта CHAR(3) NOT NULL,
            Основание VARCHAR(255) NOT NULL,
            Сумма NUMERIC(10, 2) NOT NULL CHECK (Сумма > 0),
            Дата_начисления DATE NOT NULL,
            Статус VARCHAR(30) NOT NULL,
            Заявление_id BIGINT NOT NULL REFERENCES Заявление(id) ON DELETE RESTRICT ON UPDATE CASCADE,
            Ведомство_id BIGINT NOT NULL REFERENCES Ведомство(id) ON DELETE RESTRICT ON UPDATE CASCADE
        );
        """)

        #E14-Платеж
        cursor.execute("""
        CREATE TABLE Платеж (
            id BIGINT PRIMARY KEY,
            Статус VARCHAR(30) NOT NULL,
            Валюта CHAR(3) NOT NULL,
            Сумма NUMERIC(10, 2) NOT NULL CHECK (Сумма > 0),
            Дата_и_время_платежа TIMESTAMPTZ NOT NULL,
            Способ_оплаты VARCHAR(30) NOT NULL,
            Пользователь_id BIGINT NOT NULL REFERENCES Пользователь(id) ON DELETE RESTRICT ON UPDATE CASCADE
        );
        """)

        #E13__-Оплата начисления n:n разреш.
        cursor.execute("""
        CREATE TABLE Оплата_начисления (
            Начисление_id BIGINT NOT NULL REFERENCES Начисление(id) ON DELETE RESTRICT ON UPDATE CASCADE,
            Платёж_id BIGINT NOT NULL REFERENCES Платеж(id) ON DELETE RESTRICT ON UPDATE CASCADE,
            Сумма_оплаты NUMERIC(10, 2) NOT NULL CHECK (Сумма_оплаты > 0),
            Дата_и_время_оплаты TIMESTAMPTZ NOT NULL,
            Признак_закрытия BOOLEAN NOT NULL DEFAULT TRUE,
            PRIMARY KEY (Начисление_id, Платёж_id)
        );
        """)

        #E15-Запись на приём
        cursor.execute("""
        CREATE TABLE Запись_на_приём (
            id BIGINT PRIMARY KEY,
            Дата_приема DATE NOT NULL,
            Время_начала TIME NOT NULL,
            Время_окончания TIME NOT NULL,
            Адрес TEXT NOT NULL,
            Пользователь_id BIGINT NOT NULL REFERENCES Пользователь(id) ON DELETE CASCADE ON UPDATE CASCADE,
            Услуга_id BIGINT NOT NULL REFERENCES Услуга(id) ON DELETE RESTRICT ON UPDATE CASCADE,
            Заявление_id BIGINT NOT NULL UNIQUE REFERENCES Заявление(id) ON DELETE CASCADE ON UPDATE CASCADE,
            CHECK (Время_окончания > Время_начала)
        );
        """)

        # E16- Жалоба
        cursor.execute("""
        CREATE TABLE Жалоба (
            id BIGINT PRIMARY KEY,
            Номер VARCHAR(50) NOT NULL UNIQUE,
            Дата_и_время_подачи TIMESTAMPTZ NOT NULL,
            Содержание TEXT NOT NULL,
            Тип VARCHAR(50) NOT NULL,
            Статус VARCHAR(30) NOT NULL,
            Пользователь_id BIGINT NOT NULL REFERENCES Пользователь(id) ON DELETE RESTRICT ON UPDATE CASCADE,
            Ведомство_id BIGINT NOT NULL REFERENCES Ведомство(id) ON DELETE RESTRICT ON UPDATE CASCADE,
            Заявление_id BIGINT NOT NULL REFERENCES Заявление(id) ON DELETE RESTRICT ON UPDATE CASCADE
        );
        """)

        # E17-Решение по жалобе
        cursor.execute("""
        CREATE TABLE Решение_по_жалобе (
            id BIGINT PRIMARY KEY,
            Вид_решения VARCHAR(50) NOT NULL,
            Решение TEXT NOT NULL,
            Дата_и_время_решения TIMESTAMPTZ NOT NULL,
            Пользователь_id BIGINT NOT NULL REFERENCES Пользователь(id) ON DELETE RESTRICT ON UPDATE CASCADE,
            Жалоба_id BIGINT NOT NULL UNIQUE REFERENCES Жалоба(id) ON DELETE CASCADE ON UPDATE CASCADE
        );
        """)

        #E18-Журнал аудита
        cursor.execute("""
        CREATE TABLE Журнал_аудита (
            id BIGINT PRIMARY KEY,
            Дата_и_время_события TIMESTAMPTZ NOT NULL,
            Тип_действия VARCHAR(50) NOT NULL,
            Тип_сущности VARCHAR(50) NOT NULL,
            Старое_значение TEXT,
            Новое_значение TEXT
        );
        """)

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

create_tables()
