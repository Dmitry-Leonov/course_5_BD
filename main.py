from src.utils.utils import *
from colorama import Fore


def main():
    create_table()

    while True:
        task = input(Fore.GREEN +
                     "Введите 1, чтобы получить список всех компаний и количество вакансий у каждой компании\n"
                     "Введите 2, чтобы получить список всех вакансий с указанием названия компании, "
                     "названия вакансии и зарплаты и ссылки на вакансию\n"
                     "Введите 3, чтобы получить среднюю зарплату по вакансиям\n"
                     "Введите 4, чтобы получить список всех вакансий, у которых зарплата выше средней по всем вакансиям\n"
                     "Введите 5, чтобы получить список всех вакансий, в названии которых содержатся переданные в метод слова\n"
                     "Введите Стоп или Stop, чтобы завершить работу\n"
                     + Fore.RESET)

        if task == "Стоп" or task == "Stop":
            print(Fore.GREEN + "Работа с базой завершена" + Fore.RESET)
            break
        elif task == '1':
            get_companies_and_vacancies_count()
            print()
        elif task == '2':
            get_all_vacancies()
            print()
        elif task == '3':
            get_avg_salary()
            print()
        elif task == '4':
            get_vacancies_with_higher_salary()
            print()
        elif task == '5':
            keyword = input(Fore.GREEN + "Введите ключевой слово для поиска вакансии\n" + Fore.RESET)
            get_vacancies_with_keyword(keyword)
            print()
        else:
            print(Fore.GREEN + "Неправильный запрос" + Fore.RESET)

    # get_companies_and_vacancies_count()

    # get_all_vacancies()

    # get_avg_salary()

    # get_vacancies_with_higher_salary()

    # keyword = 'Python'
    # get_vacancies_with_keyword(keyword)


if __name__ == '__main__':
    main()
