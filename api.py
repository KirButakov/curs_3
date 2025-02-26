import requests
from typing import List, Dict, Optional


def get_employer_data(employer_id: str) -> Optional[Dict]:
    """
    Получает данные о работодателе по его ID через API hh.ru.

    :param employer_id: ID работодателя.
    :return: Словарь с данными о работодателе или None, если данные не получены.
    """
    url = f"https://api.hh.ru/employers/{employer_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


def get_vacancies_data(employer_id: str) -> List[Dict]:
    """
    Получает список вакансий для указанного работодателя через API hh.ru.

    :param employer_id: ID работодателя.
    :return: Список словарей с данными о вакансиях.
    """
    url = f"https://api.hh.ru/vacancies?employer_id={employer_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['items']
    return []
