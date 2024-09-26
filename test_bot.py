import sys
import datetime
from os import makedirs, path
import os

import asyncio
from logger import logger
from aiogram import Bot, Dispatcher, types, enums
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters.command import Command
from aiogram import F
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.keyboard import InlineKeyboardBuilder
import io
import time
from rest_api import RestApi
from lesson import Lesson

from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException, JSONDecodeError, ReadTimeout

class TgBot:
    def __init__(self, tg_api_key, site_url, rest_api_url, rest_api_key, uploads_path, tg_course_chat_id, tg_channel_id):
        self.uploads_path = uploads_path
        self.course_chat_id = tg_course_chat_id
        self.channel_id = tg_channel_id
        self.site_url = site_url
        self.bot = Bot(token=tg_api_key, default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        ))
        self.dp = Dispatcher()
        self.rest = RestApi(rest_api_url, rest_api_key)
        self.exceptions = [HTTPError, ConnectionError, Timeout, RequestException, JSONDecodeError, ReadTimeout]
        self.setup_handlers()
        
        self.running_users = []
        asyncio.run(self.start_bot())
        
    def get_start_param(self, text):
        # Extracts the parameter value from the sent /start command.
        return text.split()[1] if len(text.split()) > 1 else None

    async def start_lessons(self, user_id, first_name, lk_url: str):
        # Don't start for already running users
        if str(user_id) in self.running_users:
            return
        
        lesson_timings = [
            # [0.05,0.05,0.05,0.05,0.05,0.05,     0.05,0.05,0.05,0.05,0.05,0.05,0.05],
            # [1,0.05,0.05,0.05,0.05,0.05,     0.05,0.05,0.05,0.05,0.05,0.05,0.05],
            # [0.05,0.05,0.05,0.05,0.05,0.05,     0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05],
            # [0.05,0.05,0.05,0.05,0.05,          0.05,0.05,0.05,0.05,0.05,0.05,]
            [0.1,2,58,60,60,60,     60,60,240,120,480,240,1440],
            [30,60,60,60,60,60,     30,180,180,360,180,180,1440],
            [1,59,60,60,60,60,     60,180,180,360,360,1440],
            [1,179,60,60,180,     240,240,240,120,60,60],
        ]

        try:
            ## Find last completed lesson
            current_lesson = 0
            lessons: list = self.rest.get_user_lessons(user_id)
            if len(lessons) == 0:
                return
            
            for lesson in lessons:
                if (lesson['completed'] and current_lesson + 1 < len(lessons)):
                    current_lesson += 1
                else:
                    break
            # print('Current lesson: ' + str(current_lesson + 1))
                
            ## Define next message based on deadline time
            current_step = len(lesson_timings[current_lesson]) - 1
            time_dl = time.strptime(lessons[current_lesson]['deadline'], '%Y-%m-%d %H:%M:%S')
            # mins till deadline
            mins_left = (time.mktime(time_dl) - time.time()) / 60
            # add last step delay because it's after deadline
            if (current_lesson < 3):
                mins_left += lesson_timings[current_lesson][-1]
            mins_sum = 0
            while True:
                mins_sum += lesson_timings[current_lesson][current_step]
                if mins_sum >= mins_left or current_step == 0:
                    break
                current_step -= 1

            # elapsed since current step
            mins_elspsed = mins_sum - mins_left
            mins_delay = lesson_timings[current_lesson][current_step] - mins_elspsed

            lesson_4 = Lesson(self, user_id, first_name, lk_url, lesson_timings[3], 4)
            lesson_3 = Lesson(self, user_id, first_name, lk_url, lesson_timings[2], 3, lesson_4)
            lesson_2 = Lesson(self, user_id, first_name, lk_url, lesson_timings[1], 2, lesson_3)
            lesson_1 = Lesson(self, user_id, first_name, lk_url, lesson_timings[0], 1, lesson_2)
            # lesson_1 = Lesson(self, user_id, first_name, lk_url, lesson_timings[0], 1)
            # print('[USER]: ' + str(user_id))
            # print('Current step: ' + str(current_step))
            # print('Mins left: ' + str(mins_left))
            # print('Mins sum: ' + str(mins_sum))
            # print('Mins delay: ' + str(mins_delay))
            # print('\n')
            # If mins_left is negative, bot will send the last notification every time
            # so we prevent sending that if more than 5 mins past its deadline
            if (mins_left > -5):
                self.running_users.append(str(user_id))
                await eval(f"lesson_{current_lesson + 1}.start_lesson('{user_id}', {current_step}, {mins_delay})")
        except Exception as e:
            logger.exception(e)

    def setup_handlers(self):
        ### start command - act according to user registration status
        @self.dp.message(Command("start"))
        async def start_message(message: types.Message):
            tg_user = message.from_user
            user = self.rest.get_user_link(tg_user.id)
            
            try:
                if (type(user) in self.exceptions):
                    msg = f"Произошла ошибка при попытке отправить запрос"
                    logger.error(str(user))
                    await self.bot.send_message(message.chat.id, msg)
                    return
                elif ('result' not in user):
                    logger.error(str(user))
                    return
                
                if (user['result'] == 'true' and 'link' in user):
                    # User found in database

                    # msg = f"Привет, {tg_user.first_name}! Твой личный кабинет: \n{self.site_url}{user['link']}"
                    # await self.bot.send_message(message.chat.id, msg)
                    await self.start_lessons(tg_user.id, tg_user.first_name, self.site_url + user['link'])

                    # await self.video_message(tg_user.id, 'assets/videos/tgvideo')
                    # await self.push_1(tg_user.id)
                else:
                    # User not found
                    start = self.get_start_param(message.text)
                    if (start):
                        # Has start param
                        msg = f"Добро пожаловать, {tg_user.first_name}! Сейчас мы зарегистрируем тебя и пришлём ссылку на личную страницу"
                        # await self.bot.send_message(message.chat.id, msg)

                        # Get user profile photo
                        photos_data = await self.bot.get_user_profile_photos(tg_user.id, limit=1)
                        tg_photo_url = ''
                        if photos_data.total_count > 0:
                            tg_photo = photos_data.photos[0]
                            tg_photo.sort(key=lambda p: p.file_size, reverse=True)

                            # Upload user avatar and send its relative path
                            tg_photo_file = await self.bot.get_file(tg_photo[0].file_id)
                            # print('TG PHOTO FILE: ' + str(tg_photo_file))
                            # File path usually looks like 'photos/%filename%', we take only %filename%
                            tg_photo_file_name = tg_photo_file.file_path.split('/')[-1]
                            # print('TG PHOTO NAME: ' + str(tg_photo_file_name))
                            tg_photo_url = str(tg_user.id) + '/' + tg_photo_file_name
                            # print('TG PHOTO URL: ' + str(tg_photo_url))
                            tg_photo_path = path.abspath(self.uploads_path + tg_photo_url)
                            # print('TG PHOTO LOCATION: ' + str(tg_photo_path))

                            makedirs(self.uploads_path + str(tg_user.id), exist_ok=True)
                            await self.bot.download_file(tg_photo_file.file_path, tg_photo_path)
                            # tg_photo_file = await self.bot.get_file(tg_photo[0].file_id)
                            # if (tg_photo_file is not None and 'file_path' in tg_photo_file):
                            #     tg_photo_url = tg_photo_file.file_path

                        res = self.rest.register_user(start, tg_user.id, tg_user.first_name, tg_user.last_name, tg_user.username, tg_photo_url)

                        if (type(res) in self.exceptions):
                            msg = f"Произошла ошибка при попытке отправить запрос"
                            # print(res.response.text)
                            logger.error(res.response.text)
                            await self.bot.send_message(message.chat.id, msg)
                            return
                        elif ('result' not in res):
                            msg = f"Произошла ошибка при попытке отправить запрос"
                            # print('[ERROR]: ' + res)
                            logger.error(str(res))
                            await self.bot.send_message(message.chat.id, msg)
                            return
                        
                        if (res['result'] == 'success' and 'link' in res):
                            # User registered successfully

                            # Start 1st lesson
                            await self.start_lessons(tg_user.id, tg_user.first_name, self.site_url + res['link'])
                            # pass

                            # msg = self.notifications.lesson_1_0(tg_user.first_name, res['link'])
                            # await self.bot.send_message(message.chat.id, text=msg['text'], reply_markup=msg['markup'])
                            # await self.video_message(tg_user.id, 'assets/videos/tgvideo', 'mp4')
                            # await self.push_1(tg_user.id)
                        elif (res['result'] == 'failed' and 'error' in res):
                            msg = f"Произошла ошибка при регистрации"
                            # print('[ERROR]: ' + res['error'])
                            logger.error(res['error'])
                            await self.bot.send_message(message.chat.id, msg)
                        else:
                            msg = f"Произошла неизвестная ошибка при регистрации"
                            # print('[ERROR]: ' + res)
                            logger.error(str(res))
                            await self.bot.send_message(message.chat.id, msg)
                            
                    else:
                        # No start param
                        msg = f"Пожалуйста, пройдите регистрацию на странице ..."
                        # await self.bot.send_message(message.chat.id, msg)
        
            except Exception as e:
                logger.exception(e)

        ### restart command - remove user from running list and start lessons again
        @self.dp.message(Command("restart"))
        async def restart_message(message: types.Message):
            tg_user = message.from_user
            user = self.rest.get_user_link(tg_user.id)

            try:
                if (type(user) in self.exceptions):
                    msg = f"Произошла ошибка при попытке отправить запрос"
                    logger.error(str(user))
                    await self.bot.send_message(message.chat.id, msg)
                    return
                elif ('result' not in user):
                    logger.error(str(user))
                    return
                
                if (user['result'] == 'true' and 'link' in user):
                    # User found in database
                    # Remove user from running list
                    if (str(tg_user.id) in self.running_users):
                        self.running_users.remove(str(tg_user.id))
                    # Restart lessons
                    await self.start_lessons(tg_user.id, tg_user.first_name, self.site_url + user['link'])

            except Exception as e:
                logger.exception(e)
                

        # Handle user messages in course chat
        # @self.dp.channel_post()
        @self.dp.message()
        async def chat_message(message: types.Message):
            # print(message)
            try:
                if (str(message.chat.id) == self.course_chat_id):
                    if (message.from_user):
                        print('From: ' + str(message.from_user.id))
                        res = self.rest.user_joined_chat(message.from_user.id)
                        print('RESPONSE:')
                        print(res)

            except Exception as e:
                logger.exception(e)

        @self.dp.chat_member()
        async def new_chat_member(update: types.ChatMemberUpdated):
            # print('\n')
            print(update.chat)
            # print(update.new_chat_member.status)
            # print(update.new_chat_member.user)

            ## User joined
            try:
                if (update.new_chat_member.status in ['member', 'administrator', 'creator']): # need just 'member', the others are for test
                    if (str(update.chat.id) == self.channel_id):
                        res = self.rest.user_subscribed(update.new_chat_member.user.id)
                        print('RESPONSE:')
                        print(res)

                    return

                    if ('result' not in res):
                        # REST request error
                        return
                    
                    if (res['result'] == 'success'):
                        # User subscribed successfully
                        if (str(update.chat.id) == self.course_chat_id):
                            msg = f"Добро пожаловать в чат курса!"
                        elif (str(update.chat.id) == self.channel_id):
                            msg = f"Благодарим за подписку на наш канал! Твои бонусы уже в личном кабинете"

                        # await self.bot.send_message(update.new_chat_member.user.id, msg)
                    elif (res['result'] == 'failed'):
                        # No user found or already subscribed
                        return
                    else:
                        # API returned unknown result (should not occur)
                        return
                    
                ## User left
                elif (update.new_chat_member.status == 'left'):
                    if (str(update.chat.id) == self.channel_id):
                        res = self.rest.user_unsubscribed(update.new_chat_member.user.id)
                    ## We don't check users leaving chat
                    # elif (str(update.chat.id) == self.course_chat_id):
                    #     res = self.rest.user_left_chat(update.new_chat_member.user.id)
                    
                    # print('RESPONSE:\n')
                    # print(res)

                    return

                    if ('result' not in res):
                        # REST request error
                        return
                    
                    if (res['result'] == 'success'):
                        # User unsubscribed successfully
                        if (str(update.chat.id) == self.course_chat_id):
                            msg = f"Нам жаль, что вы покинули наш чат курса"
                        elif (str(update.chat.id) == self.channel_id):
                            msg = f"Жаль, что вы покинули наш канал"

                        # await self.bot.send_message(update.new_chat_member.user.id, msg)
                        return
                    elif (res['result'] == 'failed'):
                        # No user found
                        return
                    else:
                        # API returned unknown result (should not occur)
                        return

            except Exception as e:
                logger.exception(e)

    async def start_bot(self):
        try:
            users_list = self.rest.get_users_list()
            if (users_list):
                users_list = list(map(lambda usr: {
                    'uid': usr['tg_uid'],
                    'first_name': usr['first_name'],
                    'lk_url': usr['link']
                }, users_list))
            else:
                users_list = []

            tasks = []
            tasks.append(self.dp.start_polling(self.bot))
            for user in users_list:
                # if (str(user['uid']) == '806075497'):
                tasks.append(self.start_lessons(user['uid'], user['first_name'], self.site_url + user['lk_url']))

            await asyncio.gather(*tasks)

        except Exception as e:
            logger.exception(e)