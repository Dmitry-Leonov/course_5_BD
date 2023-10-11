import requests


class HeadHunter():
    def __init__(self, company_id):
        self.company_id = company_id
        self.params = {
            'area': 1,  # Поиск по вакансиям города Москва
            'page': 0,  # Номер стартовой страницы поиска
            'per_page': 100  # Количество записей на страницу
        }

    def get_company(self):
        """Получение информации о компаниях"""
        base_url = f'https://api.hh.ru/employers/{self.company_id}/'

        response = requests.get(base_url, params=self.params)
        data = response.json()
        result = {
            'title': data['name'],
            'description': data['industries'][0]['name'] if data['industries'] else None,
            'url': data['alternate_url']
        }

        return result

    def get_vacancies(self):
        """Получение информации о вакансиях"""
        params = {
            'area': 1,  # Поиск по вакансиям города Москва
            'page': 0,  # Номер стартовой страницы поиска
            'per_page': 100  # Количество записей на страницу
        }

        base_url = f'https://api.hh.ru/vacancies?employer_id={self.company_id}'

        response = requests.get(base_url, params=self.params)
        data = response.json().get('items', [])

        result = []
        for i in data:
            result.append({
                'title': i['name'],
                'salary_from': i['salary']['from'] if i['salary'] else None,
                'salary_to': i['salary']['to'] if i['salary'] else None,
                'url': i['alternate_url']
            })


        return result