import requests.models
import lxml.html
from requests import get
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'


def get_response(url: str, *args, **kwargs) -> requests.models.Response:  # Возвращает ответ по указанному url
    return get(url, *args, **kwargs)


def get_html(resp: requests.models.Response) -> str:  # Возвращает html-код страницы, полученной в запросе
    return resp.text


def get_tree(html_text: str) -> lxml.html.HtmlElement:
    return lxml.html.document_fromstring(html_text)


response = get_response('https://krasnodar.hh.ru/search/vacancy?text=python+junior&area=53', headers={
    'user-agent': USER_AGENT
})
html_text = get_html(response)
tree = get_tree(html_text)
print(tree.xpath('//*[@id="HH-React-Root"]/div/div[3]/div[1]/div/div[1]/div[1]/div/h1/text()[1]'))




