import os
from dotenv import load_dotenv
from api import get_employer_data, get_vacancies_data
from database import create_database, create_tables, insert_employer_data, insert_vacancy_data
from db_manager import DBManager
import psycopg2


def main():
    # Загрузка переменных окружения
    load_dotenv()
    db_name = os.getenv('DB_NAME', 'hh_vacancies')
    user = os.getenv('DB_USER', 'postgres')
    password = os.getenv('DB_PASSWORD', 'password')
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', '5432')

    # Создание базы данных и таблиц (если они не существуют)
    create_database(db_name, user, password, host, port)
    create_tables(db_name, user, password, host, port)

    # Подключение к базе данных
    conn = psycopg2.connect(dbname=db_name, user=user, password=password, host=host, port=port)

    # Проверяем, есть ли данные в таблице employers
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM employers")
        employers_count = cur.fetchone()[0]

    # Если таблица employers пуста, заполняем её данными
    if employers_count == 0:
        employer_ids = ['15478', '2180', '3529', '1740', '78638', '2748', '3776', '4181', '3127', '64174']
        for employer_id in employer_ids:
            employer_data = get_employer_data(employer_id)
            if employer_data:
                insert_employer_data(conn, employer_data)

            vacancies_data = get_vacancies_data(employer_id)
            for vacancy in vacancies_data:
                insert_vacancy_data(conn, vacancy)

        conn.commit()
        print("Данные о компаниях и вакансиях загружены.")
    else:
        print("Данные уже загружены.")

    conn.close()

    # Работа с DBManager
    db_manager = DBManager(db_name, user, password, host, port)

    print("\nКомпании и количество вакансий:")
    for company, count in db_manager.get_companies_and_vacancies_count():
        print(f"{company}: {count} вакансий")

    print("\nСредняя зарплата по вакансиям:", db_manager.get_avg_salary())

    print("\nВакансии с зарплатой выше средней:")
    for vacancy in db_manager.get_vacancies_with_higher_salary():
        print(vacancy)

    keyword = "python"
    print(f"\nВакансии с ключевым словом '{keyword}':")
    for vacancy in db_manager.get_vacancies_with_keyword(keyword):
        print(vacancy)


if __name__ == "__main__":
    main()
