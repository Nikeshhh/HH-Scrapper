import parser
import api_vk
import os


def main():  # Основная функция для работы бота
    my_vk_api = api_vk.MyVkApi(os.getenv('VK_API_TOKEN'))  # Авторизация бота в api через токен
    my_parser = parser.MyHHParser('https://krasnodar.hh.ru/search/vacancy?text=python+junior&area=53', 10, my_vk_api)
    my_parser.get_cycle()  # Основной цикл работы бота


if __name__ == '__main__':
    main()
