import psycopg2

from src.db.config import host, database, user, password, port


class DBManager:
    def __init__(self):
        pass

    def create_table(self):
        """Создание таблиц"""
        try:
            # Подключение к базе данных
            connection = psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password,
                port=port)
            connection.autocommit = True

            with connection.cursor() as cursor:
                cursor.execute("""
                        create table if not exists companies(
                        company_id int primary key,
                        title varchar(255),
                        description text,
                        url text
                        )
                        """)
                print('Таблица company успешно создана')

                cursor.execute("""
                        create table if not exists vacancies(
                        vacancies_id serial primary key,
                        title varchar(255),
                        salary_from int,
                        salary_to int,
                        url text,
                        company_id int references companies(company_id)
                        )
                        """)
                print('Таблица vacancies успешно создана')
        except Exception as e:
            print("Ошибка подключения к базе данных", e)
        finally:
            if connection:
                connection.close()

    def load_table_company(self, company, title, description, url):
        """Заполнение таблицы компании"""
        try:
            # Подключение к базе данных
            connection = psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password,
                port=port)
            connection.autocommit = True

            with connection.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO companies (company_id, title, description, url) VALUES (%s, %s, %s, %s)',
                    (company, title, description, url))
                print(f'Данные по компании "{title}" успешно загружены')

        except Exception as e:
            print("Ошибка подключения к базе данных", e)
        finally:
            if connection:
                connection.close()

    def load_table_vacancy(self, title, salary_from, salary_to, url, company_id):
        """Загрузка таблицы вакансии"""
        try:
            # Подключение к базе данных
            connection = psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password,
                port=port)
            connection.autocommit = True

            with connection.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO vacancies (vacancies_id, title, salary_from, salary_to, url, company_id) VALUES (DEFAULT, %s, %s, %s, %s, %s)',
                    (title, salary_from, salary_to, url, company_id))

        except Exception as e:
            print("Ошибка подключения к базе данных", e)
        finally:
            if connection:
                connection.close()

    def clear_tables(self):
        """Очистка таблиц companies и vacancies от данных"""
        try:
            # Подключение к базе данных
            connection = psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password,
                port=port)
            connection.autocommit = True

            with connection.cursor() as cursor:
                cursor.execute('DELETE FROM vacancies')
                cursor.execute('DELETE FROM companies')

        except Exception as e:
            print("Ошибка при очистке таблиц от данных", e)
        finally:
            if connection:
                connection.close()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и вакансий у каждой компании"""
        connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port)

        with connection.cursor() as cursor:
            cursor.execute("""
                select companies.title, count(vacancies.*)
                from companies
                join vacancies using (company_id) 
                group by companies.title
            """)
            results = cursor.fetchall()
        if connection:
            connection.close()
        return results

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию"""
        connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port)

        with connection.cursor() as cursor:
            cursor.execute("""
                select companies.title, vacancies.title, vacancies.salary_from, vacancies.salary_to, vacancies.url
                from companies
                join vacancies using (company_id) 
            """)
            results = cursor.fetchall()
        return results

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port)

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT CAST(ROUND(AVG(salary_to)) as INTEGER) 
                FROM vacancies
            """)
            results = cursor.fetchall()
        return results

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port)

        with connection.cursor() as cursor:
            cursor.execute("""
                select title, salary_from, salary_to, url
                from vacancies 
                where salary_to > (SELECT CAST(ROUND(AVG(salary_to)) as INTEGER) 
                FROM vacancies)
            """)
            results = cursor.fetchall()
        return results

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port)

        with connection.cursor() as cursor:
            cursor.execute(f"SELECT title, salary_from, salary_to, company_id "
                           f"FROM vacancies WHERE title LIKE('%{keyword}%')")
            results = cursor.fetchall()
        return results
