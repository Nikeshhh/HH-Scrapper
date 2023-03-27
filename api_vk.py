import os
import vk_api
from vk_api.utils import get_random_id

TARGET_USER_ID = 195721094
vk_token = os.getenv('VK_API_TOKEN')


class MyVkApi:
    """
    Класс, упрощающий работу с vk_api.
    """
    def __init__(self, token):
        self.vk = vk_api.VkApi(token=token).get_api()

    def send_message(self, message, user_id=None):
        if user_id is None:
            user_id = TARGET_USER_ID
        self.vk.messages.send(
            user_id=user_id,
            random_id=get_random_id(),
            message=message
        )


if __name__ == '__main__':
    api = MyVkApi(vk_token)
    api.send_message('qwer')
