import psycopg2
from psycopg2 import sql
from typing import Optional, Dict


def create_database(db_name: str, user: str, password: str, host: str = 'localhost', port: str = '5432') -> None:
    """
    Создает базу данных PostgreSQL, если она не существует.

    """
    conn = psycopg2.connect(dbname='postgres', user=user, password=password, host=host, port=port)
    conn.autocommit = True
    cur = conn.cursor()

    # Проверяем, существует ли база данных
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
    exists = cur.fetchone()

    if not exists:
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
        print(f"База данных {db_name} создана.")
    else:
        print(f"База данных {db_name} уже существует.")

    cur.close()
    conn.close()


def create_tables(db_name: str, user: str, password: str, host: str = 'localhost', port: str = '5432') -> None:
    """
    Создает таблицы в базе данных PostgreSQL, если они не существуют.

    """
    conn = psycopg2.connect(dbname=db_name, user=user, password=password, host=host, port=port)
    cur = conn.cursor()

    # Проверяем, существует ли таблица employers
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'employers'
        );
    """)
    employers_table_exists = cur.fetchone()[0]

    # Проверяем, существует ли таблица vacancies
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'vacancies'
        );
    """)
    vacancies_table_exists = cur.fetchone()[0]

    if not employers_table_exists:
        cur.execute("""
            CREATE TABLE employers (
                employer_id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                website VARCHAR(255)
            );
        """)
        print("Таблица employers создана.")

    if not vacancies_table_exists:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                employer_id INTEGER REFERENCES employers(employer_id),
                title VARCHAR(255) NOT NULL,
                salary INTEGER,
                link VARCHAR(255) NOT NULL)
            );
        """)
        print("Таблица vacancies создана.")

    conn.commit()
    cur.close()
    conn.close()


def insert_employer_data(conn, employer_data: Dict) -> None:
    """
    Вставляет данные о работодателе в таблицу employers.

    :param conn: Соединение с базой данных.
    :param employer_data: Данные о работодателе.
    """
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO employers (employer_id, name, description, website)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (employer_id) DO NOTHING;
        """, (employer_data['id'], employer_data['name'], employer_data['description'], employer_data['site_url']))


def insert_vacancy_data(conn, vacancy_data: Dict) -> None:
    """
    Вставляет данные о вакансии в таблицу vacancies.

    :param conn: Соединение с базой данных.
    :param vacancy_data: Данные о вакансии.
    """
    with conn.cursor() as cur:
        salary = vacancy_data['salary']['from'] if vacancy_data['salary'] else None
        cur.execute("""
            INSERT INTO vacancies (vacancy_id, employer_id, title, salary, link)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (vacancy_id) DO NOTHING;
        """, (vacancy_data['id'], vacancy_data['employer']['id'], vacancy_data['name'], salary, vacancy_data['alternate_url']))