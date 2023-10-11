from src.api.constants import companies
from src.api.headhunter import HeadHunter
from src.db.dbmanager import DBManager


def create_table():
    """Создание и заполнение таблиц компаний и вакансий"""
    db = DBManager()
    db.create_table()
    db.clear_tables()


    # Заполнение таблицы компании
    for company in companies.values():
        api = HeadHunter(company)

        employee = api.get_company()
        db.load_table_company(company, employee['title'], employee['description'], employee['url'])

        for vacancy in api.get_vacancies():
            db.load_table_vacancy(vacancy['title'], vacancy['salary_from'], vacancy['salary_to'], vacancy['url'],
                                  company)

def get_companies_and_vacancies_count():
    """Обработка вывода запроса get_companies_and_vacancies_count()"""
    db = DBManager()
    for i in db.get_companies_and_vacancies_count():
        print(f'У компании: "{i[0]}" найдено {i[1]} вакансий')

def get_all_vacancies():
    """Обработка вывода запроса get_all_vacancies()"""
    db = DBManager()
    for i in db.get_all_vacancies():
        print(f'Компания - "{i[0]}", вакансия - "{i[1]}", зарплата - "{i[2]}-{i[3]}", ссылка на вакансию - "{i[4]}"')


def get_avg_salary():
    """Обработка вывода запроса get_avg_salary()"""
    db = DBManager()
    print(f'Средняя зарплата по всем вакансиям составляет: {db.get_avg_salary()[0][0]} рублей')

def get_vacancies_with_higher_salary():
    """Обработка вывода запроса get_vacancies_with_higher_salary()"""
    db = DBManager()
    for i in db.get_vacancies_with_higher_salary():
        print(f'вакансия - "{i[0]}", зарплата - "{i[1]}-{i[2]}", ссылка на вакансию - "{i[3]}"')

def get_vacancies_with_keyword(keyword):
    db = DBManager()
    print(f'\033[32mПо запросу "{keyword}" найдены следующие вакансии:\033[0m')
    for i in db.get_vacancies_with_keyword(keyword):
        print(f'вакансия - "{i[0]}", зарплата - "{i[1]}-{i[2]}", ссылка на вакансию - "{i[3]}"')