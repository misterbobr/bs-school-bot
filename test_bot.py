import sys
import datetime

import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F
import io
import rest_api

class TgBot:
    def __init__(self, api_key, api_url, uploads_path):
        self.api_key = api_key
        self.uploads_path = uploads_path
        self.bot = Bot(self.api_key)
        self.dp = Dispatcher()
        self.rest = rest_api.RestApi(api_url)
        self.setup_handlers()
        asyncio.run(self.start_polling())
        
    def get_start_param(self, text):
        # Extracts the parameter value from the sent /start command.
        return text.split()[1] if len(text.split()) > 1 else None

    async def message_hello(self, uid):
        file_name = "assets/videos/tgvideo"
        file_id = ''
        try:
            # Take file_id from txt file if exists
            f = open(file_name + ".txt", "r")
            file_id = f.readline()
            f.close()
        except:
            pass

        if (file_id == ''):
            video = types.FSInputFile(file_name + ".mp4")
            result = await self.bot.send_video_note(uid, video)
            f = open(file_name + ".txt", "w")
            f.write(result.video_note.file_id)
            f.close()
        else:
            result = await self.bot.send_video_note(uid, file_id)
            print('Reused File ID')

        print('File ID: ' + result.video_note.file_id)

    async def push_1(self, uid):
        now = datetime.datetime.time(datetime.datetime.now())
        msg = f"Start command at {now}: "

        try:
            await asyncio.sleep(10) # wait some time
            visited = self.rest.user_visited_lk(uid) # check if user has visited lk
            if ('result' not in visited):
                pass    # TODO process possible errors in request to api
                return
            if (visited['result'] == 'true'):
                msg += "VISITED"
            else:
                msg += "NOT VISITED"
            await self.bot.send_message(uid, msg)
        
        except Exception as e:
            msg = "Exception occured: " + e
            await self.bot.send_message(uid, msg)


    def setup_handlers(self):
        ### start command - act according to user registration status
        @self.dp.message(Command("start"))
        async def start_message(message: types.Message):
            tg_user = message.from_user
            user = self.rest.get_user_link(tg_user.id)
            
            try:
                if ('result' not in user):
                    pass    # TODO process possible errors in request to api
                    return
                
                if (user['result'] == 'true' and 'link' in user):
                    # User found in database
                    msg = f"Привет, {tg_user.first_name}! Твой личный кабинет: \n{user['link']}"
                    await self.bot.send_message(message.chat.id, msg)
                    await self.message_hello(tg_user.id)
                    await self.push_1(tg_user.id)
                else:
                    # User not found
                    start = self.get_start_param(message.text)
                    if (start):
                        # Has start param
                        msg = f"Добро пожаловать, {tg_user.first_name}! Сейчас мы зарегистрируем вас и пришлём ссылку на вашу личную страницу"
                        await self.bot.send_message(message.chat.id, msg)

                        # Get user profile photo
                        photos_data = await self.bot.get_user_profile_photos(tg_user.id, limit=1)
                        tg_photo_url = ''
                        if photos_data.total_count > 0:
                            tg_photo = photos_data.photos[0]
                            tg_photo.sort(key=lambda p: p.file_size, reverse=True)
                            # Upload user avatar and send its relative path
                            tg_photo_url = tg_user.id + '/' + tg_photo[0].file_id
                            await self.bot.download(tg_photo[0].file_id, self.uploads_path + tg_photo_url)
                            # tg_photo_file = await self.bot.get_file(tg_photo[0].file_id)
                            # if (tg_photo_file is not None and 'file_path' in tg_photo_file):
                            #     tg_photo_url = tg_photo_file.file_path

                        res = self.rest.register_user(start, tg_user.id, tg_user.first_name, tg_user.last_name, tg_user.username, tg_photo_url)
                        
                        if ('result' not in res):
                            msg = f"Произошла ошибка при попытке отправить запрос. Пожалуйста, попробуйте снова"
                            await self.bot.send_message(message.chat.id, msg)
                            return
                        
                        if (res['result'] == 'success' and 'link' in res):
                            # User registered successfully
                            msg = f"Ссылка на личный кабинет: \n{res['link']}"
                            await self.bot.send_message(message.chat.id, msg)
                            await self.message_hello(tg_user.id)
                            await self.push_1(tg_user.id)
                        elif (res['result'] == 'failed' and 'error' in res):
                            msg = f"Произошла ошибка при регистрации: \n{res['error']}"
                            await self.bot.send_message(message.chat.id, msg)
                        else:
                            msg = f"Произошла неизвестная ошибка при регистрации. Пожалуйста, попробуйте снова"
                            await self.bot.send_message(message.chat.id, msg)
                            
                    else:
                        # No start param
                        msg = f"Пожалуйста, пройдите регистрацию на странице ..."
                        await self.bot.send_message(message.chat.id, msg)
        
            except TypeError as e:
                print(e)
                

        @self.dp.message(F.text)
        async def text_message(message: types.Message):
            now = datetime.datetime.time(datetime.datetime.now())
            msg = f"{now}: {message.text}"
            await asyncio.sleep(5)
            await self.bot.send_message(message.chat.id, msg)
            pass

        @self.dp.chat_member()
        async def new_chat_member(update: types.ChatMemberUpdated):
            # print(update.new_chat_member.user)
            # print('\n')
            # print(update.new_chat_member.status)
            if (update.new_chat_member.status in ['member', 'administrator', 'creator']): # need just 'member', the others are for test
                res = self.rest.user_subscription(update.new_chat_member.user.id)
                # print('RESPONSE:\n')
                # print(res)

                if ('result' not in res):
                    # REST request error
                    return
                
                if (res['result'] == 'success'):
                    # User subscribed successfully
                    msg = f"Благодарим вас за подписку на наш канал! Ваши бонусы уже в личном кабинете"
                    await self.bot.send_message(update.new_chat_member.user.id, msg)
                elif (res['result'] == 'failed'):
                    # No user found or already subscribed
                    return
                else:
                    # API returned unknown result (should not occur)
                    return

    async def start_polling(self):
        await self.dp.start_polling(self.bot)