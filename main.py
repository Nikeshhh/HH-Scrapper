import parser
import api_vk
import os


def main():  # Основная функция для работы бота
    token = input('Input a token: ')
    my_vk_api = api_vk.MyVkApi(token)  # Авторизация бота в api через токен
    my_parser = parser.MyHHParser('https://krasnodar.hh.ru/search/vacancy?text=python+junior&area=53', 28800, my_vk_api)
    my_parser.get_cycle()  # Основной цикл работы бота


if __name__ == '__main__':
    main()
