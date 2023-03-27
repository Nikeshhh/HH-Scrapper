import parser
import api_vk
import os


def main():
    my_vk_api = api_vk.MyVkApi(os.getenv('VK_API_TOKEN'))
    my_parser = parser.MyHHParser('https://krasnodar.hh.ru/search/vacancy?text=python+junior&area=53', 10, my_vk_api)
    my_parser.get_cycle()


if __name__ == '__main__':
    main()
