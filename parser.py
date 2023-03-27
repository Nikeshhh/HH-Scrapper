import requests.models
import lxml.html
from requests import get
from time import sleep
from api_vk import MyVkApi

# User-agent - необходимый в запросе заголовок для работы парсера
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'


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

    def get_cycle(self):  # Бесконечный цикл работы бота
        while True:
            response = self.get_response(self.url, headers={'user-agent': self.user_agent})  # Получение ответа
            html_t = self.get_html(response)  # Получение html разметки в виде текста
            tree = self.get_tree(html_t)  # Создание дерева для парсинга
            self.vk.send_message(self.get_results_number(tree))  # Парсинг нужного элемента и отправление ответа в сообщении
            sleep(self.delay)  # Задержка между запросами парсера


if __name__ == '__main__':
    p = MyHHParser('https://krasnodar.hh.ru/search/vacancy?text=python+junior&area=53', 10)
    p.get_cycle()
