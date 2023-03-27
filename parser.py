import requests.models
from requests import get
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'


def get_response(url: str, *args, **kwargs) -> requests.models.Response:  # Возвращает ответ по указанному url
    return get(url, *args, **kwargs)


def get_html(resp: requests.models.Response) -> str:  # Возвращает html-код страницы, полученной в запросе
    return resp.text





headers = {
    'user-agent': USER_AGENT
}
print(get_response('https://krasnodar.hh.ru/search/vacancy?text=python+junior&area=53', headers=headers))
