import requests.models
import lxml.html
import os
import api_vk
from requests import get
from time import sleep
from api_vk import MyVkApi

# User-agent - необходимый в запросе заголовок для работы парсера
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'


class MyHHParser:
    """
    Класс парсера.
    Организует бесконечный цикл получения необходимой информации.
    """
    def __init__(self, url: str, delay: int, vk: MyVkApi):
        self.url = url
        self.delay = delay
        self.user_agent = USER_AGENT
        self.vk = vk

    @staticmethod
    def get_response(url: str, *args, **kwargs):  # Возвращает ответ от запроса по указанному url
        return get(url, *args, **kwargs)

    @staticmethod
    def get_html(resp: requests.models.Response) -> str:  # Возвращает html-код страницы, полученной в запросе
        return resp.text

    @staticmethod
    def get_tree(html_text: str) -> lxml.html.HtmlElement:  # Возвращает дерево, при помощи которого происходит парсинг
        return lxml.html.document_fromstring(html_text)

    @staticmethod
    def get_results_number(p_tree: lxml.html.HtmlElement) -> int:  # Возвращает число найденных вакансий
        path_to_num = '//*[@id="HH-React-Root"]/div/div[3]/div[1]/div/div[1]/div[1]/div/h1/text()[1]'
        return p_tree.xpath(path_to_num)[0]

    @staticmethod
    def get_salary(vac_id: int, p_tree: lxml.html.HtmlElement) -> str:
        path_to_elem = '//*[@id="a11y-main-content"]/div' + f'[{vac_id}]'
        path_to_salary = '/div/div[1]/div/div[3]/span/text()'
        alt_path_to_salary = '/div/div[1]/div[1]/div[1]/span/text()'
        salary = p_tree.xpath(f'{path_to_elem}{path_to_salary}')
        if not salary:
            salary = p_tree.xpath(f'{path_to_elem}{alt_path_to_salary}')
        if salary != [] and salary[0].startswith('Сейчас'):
            salary = []
        salary = ' '.join(list(map(lambda s: s.replace('\u202f', ''), salary)))
        if salary == '':
            salary = 'Не указано'
        return salary

    def get_vacancy_info(self, vac_id: int, p_tree: lxml.html.HtmlElement) -> dict or None:
        path_to_elem = '//*[@id="a11y-main-content"]/div' + f'[{vac_id}]'
        if not p_tree.xpath(path_to_elem):
            return
        path_to_vac_name = '/div/div[1]/div[1]/div[1]/h3/span/a/text()'
        path_to_vac_if_online = '/div/div[1]/div[1]/div[3]/h3/span/a/text()'
        path_to_employer = '/div/div[1]/div[1]/div[2]/div[1]/div[1]/div/div[1]/a/text()'
        path_to_employer_if_online = '/div/div[1]/div/div[4]/div/div[1]/div/div[1]/a/text()'
        name = p_tree.xpath(f'{path_to_elem}{path_to_vac_name}')
        salary = self.get_salary(vac_id, p_tree)
        employer = p_tree.xpath(f'{path_to_elem}{path_to_employer}')
        if not name:
            """
            Если имя компании не найдено по стандартному пути, то это значит, что вакансия просматривается и 
            имя находится по немного другому пути. Тоже самое касается работодателя,
            он находится по другому пути в таком случае.
            """
            name = p_tree.xpath(f'{path_to_elem}{path_to_vac_if_online}')
            if not name:
                return {}
            else:
                name = name[0]
            employer = p_tree.xpath(f'{path_to_elem}{path_to_employer_if_online}')
            """
            Что также касаемо работодателя, его название может быть разделено по нескольким элементам.
            """
            # TODO: Разобраться с парсингом названия работодателя
            for i in range(3, 4):
                employer.extend(p_tree.xpath(f'{path_to_elem}{path_to_employer_if_online}[{i}]'))
            employer = list(map(lambda s: s.replace('\xa0', ''), employer))
            employer = ' '.join(employer)
        else:
            # Если вакансия не просматривается, все находится по стандартным путям,
            # при этом зарплата может быть не указана

            # Соответственно достаем строки из результатов парсинга
            name = name[0]
            employer = list(map(lambda s: s.replace('\xa0', ''), employer))
            employer = employer[0]
        # Формируем словарь с необходимой информацией
        vacancy = {
            'name': name,
            'salary': salary,
            'employer': employer
        }
        return vacancy

    def get_vacs_from_page(self) -> list:  # Должна возвращать список словарей с вакансиями на странице
        response = self.get_response(self.url, headers={'user-agent': self.user_agent})  # Получение ответа
        html_t = self.get_html(response)  # Получение html разметки в виде текста
        p_tree = self.get_tree(html_t)  # Создание дерева для парсинга
        i = 2
        vac = self.get_vacancy_info(i, p_tree)
        result = []
        while vac is not None:
            vac = self.get_vacancy_info(i, p_tree)
            result.append(vac)
            i += 1
        return result[:-1]

    @staticmethod
    def create_page_vacs_message(vacancies: list) -> str:  # Возвращает отформатированный список вакансий в виде строки
        response = ''
        for vac in vacancies:
            if not vac:
                continue
            for value in vac.values():
                response += f'{value}\n'
            response += '---------\n'
        return response

    def get_cycle(self) -> None:  # Бесконечный цикл работы бота
        while True:
            vacs = self.get_vacs_from_page()
            msg = self.create_page_vacs_message(vacs)
            self.vk.send_message(msg)
            sleep(self.delay)  # Задержка между запросами парсера


if __name__ == '__main__':
    my_vk_api = api_vk.MyVkApi(os.getenv('VK_API_TOKEN'))  # Авторизация бота в api через токен
    p = MyHHParser('https://krasnodar.hh.ru/search/vacancy?text=python+junior&area=53', 20, my_vk_api)
    p.get_cycle()
