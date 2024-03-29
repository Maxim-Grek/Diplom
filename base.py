from datetime import datetime 
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import acces_token

class VkTools():
    def __init__(self, acces_token):
       self.api = vk_api.VkApi(token=acces_token)

    def get_profile_info(self, user_id):

        info, = self.api.method('users.get',
                            {'user_id': user_id,
                            'fields': 'city,bdate,sex,relation,home_town' 
                            }
                            )
        user_info = {'name': info['first_name'] + ' '+ info['last_name'],
                     'id':  info['id'],
                     'bdate': info['bdate'] if 'bdate' in info else None,
                     'home_town': info['home_town'],
                     'sex': info['sex'],
                     'city': info['city']['id']
                     }
        return user_info
    
    def serch_users(self, params):

        sex = 1 if params['sex'] == 2 else 2
        city = params['city']
        curent_year = datetime.now().year
        user_year = int(params['bdate'].split('.')[2])
        age = curent_year - user_year
        age_from = age - 5
        age_to = age + 5

        users = self.api.method('users.search',
                                {'count': 30,
                                 'offset': 0,
                                 'age_from': age_from,
                                 'age_to': age_to,
                                 'sex': sex,
                                 'city': city,
                                 'status': 6,
                                 'is_closed': False
                                }
                            )
        try:
            users = users['items']
        except KeyError:
            return []
        
        res = []

        for user in users:
            if user['is_closed'] == True:
                res.append({'id' : user['id'],
                            'name': user['first_name'] + ' ' + user['last_name']
                           }
                           )
            continue
        return res
    def get_photos(self, user_id):
        photos = self.api.method('photos.get',
                                 {'user_id': user_id,
                                  'album_id': 'profile',
                                  'extended': 1
                                 }
                                )
        try:
            photos = photos['items']
        except KeyError:
            return []
        
        res = []

        for photo in photos:
            res.append({'owner_id': photo['owner_id'],
                        'id': photo['id'],
                        'likes': photo['likes']['count'],
                        'comments': photo['comments']['count'],
                        }
                        )
            
        res.sort(key=lambda x: x['likes']+x['comments']*10, reverse=True)
         
        return res
    def show_found_person(self, user_id):
        print(self.get_profile_info())
        if self.get_profile_info() == None:
            self.send_msg(user_id,
                          f'Все анекты ранее были просмотрены. Будет выполнен новый поиск. '
                          f'Измените критерии поиска (возраст, город). '
                          f'Введите возраст поиска'
                          f'в формате : 21-35 или конкретно 30')
            for event in self.vk_api.longpoll.listen():
             if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    age = event.text
                    self.serch_users(self, params)
                    return   
if __name__ == '__main__':
    bot = VkTools(acces_token)
    params = bot.get_profile_info(789657038)
    users = bot.serch_users(params)
    print(bot.get_photos(users[2]['id']))
