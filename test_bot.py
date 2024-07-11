import sys

from telebot import TeleBot, types
from telebot.util import quick_markup
import rest_api

class TgBot:
    def __init__(self, api_key, api_url):
        self.api_key = api_key
        self.bot = TeleBot(self.api_key)
        self.rest = rest_api.RestApi(api_url)
        self.setup_handlers()
        self.start_polling()

        
    def get_start_param(self, text):
        # Extracts the parameter value from the sent /start command.
        return text.split()[1] if len(text.split()) > 1 else None

    def check_user_exists(self, uid):
        pass

    def setup_handlers(self):
        ### start command - act according to user registration status
        @self.bot.message_handler(commands=["start"])
        def start_message(message: types.Message):
            tg_user = message.from_user
            user = self.rest.get_user(tg_user.id)
            
            if ('result' not in user):
                pass    # TODO process possible errors in request to api
                return
            
            if (user['result'] == 'true'):
                # User found in database
                msg = f"Привет, {tg_user.first_name}!"
                self.bot.send_message(message.chat.id, msg)
            else:
                # User not found
                start = self.get_start_param(message.text)
                if (start):
                    # Has start param
                    msg = f"Добро пожаловать!, {tg_user.first_name}! Сейчас мы зарегистрируем вас и пришлём ссылку на вашу личную страницу"
                    self.bot.send_message(message.chat.id, msg)

                    # Get user profile photo
                    photos_data = self.bot.get_user_profile_photos(tg_user.id, limit=1)
                    tg_photo = photos_data.photos[0]
                    tg_photo.sort(key=lambda p: p.file_size, reverse=True)
                    tg_photo_url = self.bot.get_file_url(tg_photo[0].file_id)

                    res = self.rest.register_user(start, tg_user.id, tg_user.first_name, tg_user.last_name, tg_user.username, tg_photo_url)
                    
                    if ('result' not in res):
                        msg = f"Произошла ошибка при попытке отправить запрос. Пожалуйста, попробуйте снова"
                        self.bot.send_message(message.chat.id, msg)
                        return
                    
                    if (res['result'] == 'success'):
                        # User registered successfully
                        msg = f"Ссылка на личный кабинет \n{res['link']}"
                        self.bot.send_message(message.chat.id, msg)
                    else:
                        msg = f"Произошла ошибка при регистрации. Пожалуйста, попробуйте снова"
                        self.bot.send_message(message.chat.id, msg)
                        
                else:
                    # No start param
                    msg = f"Пожалуйста, пройдите регистрацию на странице ..."
                    self.bot.send_message(message.chat.id, msg)
                
                
            # if user:
            #     if user.verified_status.verified:
            #         self.bot.send_message(
            #             message.chat.id, "Добро пожаловать в бота"
            #         )
            # else:
            #     pass

        @self.bot.message_handler(commands=["kill"])
        def kill_command(message: types.Message):
            if message.text.endswith(self.api_key):
                self.bot.stop_bot()
                sys.exit()


        @self.bot.message_handler(content_types=["text"])
        def text_message(message: types.Message):
            pass


    def start_polling(self):
        self.bot.infinity_polling()