import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from config import comunity_token, acces_token
from base import VkTools

class BotInterface():

    def __init__(self,comunity_token, acces_token):
        self.interface = vk_api.VkApi(token=comunity_token)
        self.api = VkTools(acces_token)
        self.params = None


    def message_send(self, user_id, message, attachment=None):
        self.interface.method('messages.send',
                                {'user_id': user_id,
                                'message': message,
                                'attachment': attachment,
                                'random_id': get_random_id()
                                }
                                )
        
    def event_handler(self):
        longpoll = VkLongPoll(self.interface)

        
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                command = event.text.lower()

                if command == 'привет':
                    self.params = self.api.get_profile_info(event.user_id)
                    self.message_send(event.user_id, f'здравствуй {self.params["name"]}')
                    
                elif command == 'поиск':
                        users = self.api.serch_users(self.params)
                        user = users.pop()
                    
                        bot.info(user_id)
                        bot.write_msg(event.user_id, f'Встречайте')
                        bot.user_info(first_name, last_name, user_id, offset)
                    
                        photos_user = self.api.get_photos(user['id'])                  
                        attachment = ''
                        for num, photo in enumerate(photos_user):
                        attachment += f'photo{photo["owner_id"]}_{photo["id"]}'
                        if num == 2:
                           continue
                elif command == 'вперёд':
                    for i in line:
                        offset += 1
                        bot.serch_users(first_name, last_name, user_id, offset)
                        break

                    else:
                        bot.write_msg(event.user_id, 'Введите заново')

if __name__ == '__main__':
    bot = BotInterface(comunity_token, acces_token)
    bot.event_handler()
