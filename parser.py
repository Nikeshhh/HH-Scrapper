from requests import get
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'


def get_api(url: str, *args, **kwargs) -> str:
    return get(url, *args, **kwargs).text




headers = {
    'user-agent': USER_AGENT
}
print(get_api('https://krasnodar.hh.ru/search/vacancy?text=python+junior&area=53', headers=headers))
