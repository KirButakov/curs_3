# Проект: Парсинг вакансий с hh.ru и работа с базой данных PostgreSQL

Этот проект позволяет получать данные о компаниях и их вакансиях с сайта hh.ru, сохранять их в базу данных PostgreSQL и работать с этими данными через удобный интерфейс.

## Основные функции

- Получение данных о компаниях и вакансиях через API hh.ru.
- Создание базы данных PostgreSQL и таблиц для хранения данных.
- Заполнение таблиц данными о компаниях и вакансиях.
- Получение данных из базы данных:
  - Список компаний и количество вакансий.
  - Список всех вакансий с указанием компании, названия, зарплаты и ссылки.
  - Средняя зарплата по вакансиям.
  - Список вакансий с зарплатой выше средней.
  - Список вакансий по ключевому слову.

## Как запустить проект

1. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   
## Настройте базу данных:

- Убедитесь, что у вас установлен PostgreSQL.
- Создайте базу данных (например, hh_vacancies).
- Настройте переменные окружения в файле .env: 
  - DB_NAME=hh_vacancies
  - DB_USER=ваш_пользователь_postgres
  - DB_PASSWORD=ваш_пароль_postgres
  - DB_HOST=localhost
  - DB_PORT=5432

## Запустите проект:

python main.py

Программа выполнит следующие действия:
  - Создаст базу данных и таблицы (если они не существуют).
  - Загрузит данные о компаниях и вакансиях через API hh.ru.
  - Выведет результаты в консоль.

## Структура проекта

- .env — файл с переменными окружения.
- .gitignore — файл для игнорирования ненужных файлов.
- requirements.txt — файл с зависимостями.
- api.py — модуль для работы с API hh.ru.
- database.py — модуль для работы с базой данных.
- db_manager.py — модуль с классом DBManager для работы с данными.
- main.py — точка входа в программу.