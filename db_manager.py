import psycopg2
from typing import List, Optional, Dict


class DBManager:
    """
    Класс для управления базой данных PostgreSQL.
    """

    def __init__(self, dbname: str, user: str, password: str, host: str = 'localhost', port: str = '5432'):
        """
        Инициализирует соединение с базой данных.

        """
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

    def get_companies_and_vacancies_count(self) -> List[tuple]:
        """
        Получает список всех компаний и количество вакансий у каждой компании.

        :return: Список кортежей (название компании, количество вакансий).
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.name, COUNT(v.vacancy_id) 
                FROM employers e 
                LEFT JOIN vacancies v ON e.employer_id = v.employer_id 
                GROUP BY e.name
            """)
            return cur.fetchall()

    def get_all_vacancies(self) -> List[tuple]:
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.

        :return: Список кортежей (название компании, название вакансии, зарплата, ссылка).
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.name, v.title, v.salary, v.link 
                FROM vacancies v 
                JOIN employers e ON v.employer_id = e.employer_id
            """)
            return cur.fetchall()

    def get_avg_salary(self) -> Optional[float]:
        """
        Получает среднюю зарплату по вакансиям.

        :return: Средняя зарплата или None, если данных нет.
        """
        with self.conn.cursor() as cur:
            cur.execute("SELECT AVG(salary) FROM vacancies")
            result = cur.fetchone()
            return result[0] if result else None

    def get_vacancies_with_higher_salary(self) -> List[tuple]:
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.

        :return: Список кортежей с данными о вакансиях.
        """
        avg_salary = self.get_avg_salary()
        if avg_salary:
            with self.conn.cursor() as cur:
                cur.execute("SELECT * FROM vacancies WHERE salary > %s", (avg_salary,))
                return cur.fetchall()
        return []

    def get_vacancies_with_keyword(self, keyword: str) -> List[tuple]:
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова.

        :param keyword: Ключевое слово для поиска.
        :return: Список кортежей с данными о вакансиях.
        """
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM vacancies WHERE title ILIKE %s", (f'%{keyword}%',))
            return cur.fetchall()