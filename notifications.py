# from test_bot import TgBot
import asyncio
from aiogram import types
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.utils.keyboard import InlineKeyboardBuilder

class Notifications:

    # def __init__(self, bot: TgBot, tg_user: types.User, lk_url: str):
    def __init__(self, bot, tg_user: types.User, lk_url: str):
        self.bot = bot
        self.tg_user = tg_user
        self.lk_url = lk_url
    #     self.session = requests.Session()

    def read_local_file_id(self, file_name):
            # file_name = "assets/videos/tgvideo"
            file_id = None
            try:
                # Take file_id from txt file if exists
                f = open(file_name + ".txt", "r")
                file_id = f.readline()
                f.close()
            except Exception as e:
                print(e)
            finally:
                return file_id
            
    def write_local_file_id(self, file_name, file_id):
        try:
            f = open(file_name + ".txt", "w")
            f.write(file_id)
            f.close()
        except Exception as e:
            print(e)
            
    async def photo_message(self, uid, file_name):
        file_id = self.read_local_file_id(file_name)
        if (file_id):
            result = await self.bot.bot.send_photo(uid, file_id)
            print('Reused File ID')
        else:
            photo = types.FSInputFile(file_name)
            result = await self.bot.bot.send_photo(uid, photo)
            file_id = result.photo[0].file_id
            self.write_local_file_id(file_name, file_id)

        print('File ID: ' + file_id)

    async def group_message(self, uid, files: list[str]):
        media_group = MediaGroupBuilder()
        for file_name in files:
            file_id: str = self.read_local_file_id(file_name)
            if (file_id):
                media_group.add_photo(media=file_id)
            else:
                photo = types.FSInputFile(file_name)
                media_group.add_photo(media=photo)
        result = await self.bot.bot.send_media_group(uid, media=media_group.build())

        for i in range (0, len(result)):
            file_id = result[i].photo[0].file_id
            self.write_local_file_id(files[i], file_id)
            print(f"File {files[i]} ID: " + file_id)

    async def video_message(self, uid, file_name):
        file_id = self.read_local_file_id(file_name)
        if (file_id):
            result = await self.bot.bot.send_video_note(uid, file_id)
            print('Reused File ID')
        else:
            video = types.FSInputFile(file_name)
            result = await self.bot.bot.send_video_note(uid, video)
            print(result)
            file_id = result.video_note.file_id if result.video_note else result.video.file_id
            self.write_local_file_id(file_name, file_id)

        print('File ID: ' + file_id)

    async def lesson_1_0(self):
        builder = InlineKeyboardBuilder()
        msg =   f'Привет, {self.tg_user.first_name}! Это Ренат Шагабутдинов и академия Bonnie&Slide.'\
                ' <b>И мы приветствуем тебя на курсе "Сводные таблицы в Excel и Google Таблицах"</b>.'\
                ' Каждый день мы получаем десятки сообщений с вопросами о том, как создавать отчёты быстро, как создавать'\
                ' понятные таблицы и что делать с формулами. По этой причине мы и решили запустить этот'\
                ' 4-х дневный курс.'\
                ' \n\nВажное об этом курсе:'\
                ' \n🤖 Каждый день ты будешь получать всю важную информацию в этом боте, а уроки и'\
                ' домашние задания будут доступны в твоем личном кабинете;'\
                ' \n⏱️ На выполнение основной домашней работы у тебя есть 24 часа;'\
                ' \n🪙 За выполненные домашки ты будешь получать монеты, которые можно'\
                ' конвертировать в скидку до 40% для оплаты нашего флагманского курса;'\
                ' \n🫶🏼 <b>Но самое важное и крутое - на каждую домашку ты будешь получать разбор'\
                ' прямо от меня в личных сообщениях</b>'\
                ' \n\nЗа ближайшие 4 дня ты из точки, в которой не знаешь как использовать сводные таблицы'\
                ' или тратишь на них кучу времени, раздражаешься от работы в таблицах, не знаешь'\
                ' лайфхаков, придешь в точку, в которой не просто поймёшь этот инструмент, но и сразу'\
                ' внедришь в свою работу, тем самым экономя время на реально интересные задачи .'\
                ' \n\n<b>В общем, скорее кликай по кнопке в свой личный кабинет, смотри как устроен наш'\
                ' курс и проходи первый урок</b>'
        
        builder.row(types.InlineKeyboardButton(
            text='Начать обучение',
            url=self.lk_url)
        )
        
        await self.bot.bot.send_message(self.tg_user.id, text=msg, reply_markup=builder.as_markup())
        await asyncio.sleep(1)
        await self.video_message(self.tg_user.id, 'assets/videos/circles/1.mov')
        # return {
        #     'text': msg,
        #     'markup': builder.as_markup()
        # }

    async def lesson_1_1(self):
        builder = InlineKeyboardBuilder()
        msg =   'Мы хотим, чтобы этот курс помог тебе облегчить свою рабочую рутину и пересмотреть'\
                ' свои отношения с таблицами, поэтому очень рады, что ты здесь!'\
                ' \n\n🎁<b>Забирай по кнопке внизу наш первый подарок: гайд на 35 страниц "Топ-3'\
                ' механики по ускорению работы с помощью Google Таблиц и Excel на примере'\
                ' реальных кейсов"</b>'
        
        builder.row(types.InlineKeyboardButton(
            text='Забрать гайд',
            url=self.lk_url)
        )
        
        photos = [
            'assets/images/1-1.png',
            'assets/images/1-2.png'
        ]
        await self.group_message(self.tg_user.id, photos)
        await self.bot.bot.send_message(self.tg_user.id, text=msg, reply_markup=builder.as_markup())

    async def lesson_1_2(self):
        builder = InlineKeyboardBuilder()
        msg =   '<b>Мы понимаем, что учиться хочется у лучших, а доверять хочется настоящим экспертам</b>'\
                ' \n\nНаша академия Bonnie&Slide выпустила уже более 80 000 студентов, среди которых'\
                ' сотрудники более 100 компаний, которые каждый день работают с отчётами, дашбордами,'\
                ' формулами📈📊'\
                ' \nПоэтому и на этом мини-курсе, и на наших флагманских курсах мы ставим себе задачу дать'\
                ' тебе практические навыки и максимальную обратную связь'\
                ' \n<i>Ты можешь посмотреть, что говорят о нас люди с таким же запросом как у тебя, которые'\
                ' уже окончили наши курсы по Excel и Google Таблицам</i>'
        
        builder.row(types.InlineKeyboardButton(
            text='Прочитать больше отзывов',
            url="https://yandex.ru")
        )
        
        photos = [
            'assets/images/1-3.png',
            'assets/images/1-4.png'
        ]
        await self.group_message(self.tg_user.id, photos)
        await self.bot.bot.send_message(self.tg_user.id, text=msg, reply_markup=builder.as_markup())

    async def lesson_1_3(self):
        builder = InlineKeyboardBuilder()
        msg =   f'<b>{self.tg_user.first_name}, Excel и Google Таблицы почти всемогущи ведь они:</b>'\
                ' \n• позволяют быстро суммировать, группировать и анализировать большие объемы данных;'\
                ' \n• обладают интуитивно понятным интерфейсом, который помогает без глубоких знаний'\
                ' легко создавать сложные отчеты;'\
                ' \n• предоставляют мощные инструменты для анализа данных: вычисление средних значений,'\
                ' медиан, суммирование и нахождение процентных долей.'\
                ' \n\nПомимо этого Google Таблицы интегрированы с искусственным интеллектом, что позволяет'\
                ' создавать сводные таблицы в несколько кликов.'\
                ' \n\n🎁<b>Кстати, об искуственном интеллекте... Если ты пройдешь курс до конца, то тебя'\
                ' ждёт огненный подарок: 2 урока из нашего нового курса по нейросетям. Но и это ещё'\
                ' не всё, всего мы подготовили для тебя подарков на 60 000 руб!</b>'\
                ' \n\nСмотри первый урок, выполняй домашку, забирай первый подарок и готовься собирать'\
                ' остальные бонусы'
        
        builder.row(types.InlineKeyboardButton(
            text='Бегу смотреть',
            url=self.lk_url)
        )
        
        await self.photo_message(self.tg_user.id, 'assets/images/presents.png')
        await self.bot.bot.send_message(self.tg_user.id, text=msg, reply_markup=builder.as_markup())

    async def lesson_1_4(self):
        builder = InlineKeyboardBuilder()
        msg =   '<b>Вернулся к тебе, чтобы напомнить как проходит наш курс-игра по Excel и Google Таблицам</b>✨'\
                ' \n\n• у тебя есть 24 часа на просмотр урока и выполнение ОБЯЗАТЕЛЬНОГО домашнего задания;'\
                ' \n• если ты не посмотришь урок и не выполнишь обязательное дз в течение 6 часов, то у'\
                ' тебя сгорит 1-я жизнь, в течение 12 часов - 2-я жизнь, в течение 24 часов - последняя жизнь;'\
                ' \n• без выполнения основных заданий ты не сможешь продвинуться дальше;'\
                ' \n• есть 3 дополнительных (самых простых) задания, за выполнение которых ты также'\
                ' получаешь монеты. Например, прямо сейчас ты можешь стать "Душой компании" - вступай'\
                ' в чат этого курса, представься там и забирай монетку;'\
                ' \n• также у нас есть практические дз, на которых можно отработать тему урока, но они не'\
                ' обязательны к выполнению'\
                ' Отправляй свою основную домашку, пока у тебя не начали сгорать жизни!'
        
        builder.row(types.InlineKeyboardButton(
            text='Посмотреть первый урок',
            url=self.lk_url)
        )
        
        await self.photo_message(self.tg_user.id, 'assets/images/presents.png')
        await self.bot.bot.send_message(self.tg_user.id, text=msg, reply_markup=builder.as_markup())

    async def lesson_1_5(self):
        builder = InlineKeyboardBuilder()
        msg =   '<b>На связи Ренат, хочу поделиться с тобой, что мне дал навык работы с таблицами</b>📊'\
                ' Я работал в крупных компаниях в отделах, занимающихся бюджетированием, и мне'\
                ' нравилось писать макросы и проектировать таблицы так, чтобы многие действия и'\
                ' рутинная работа отдела автоматизировалась, а время тратилось на более сложные'\
                ' интеллектуальные задачи. С приходом в МИФ я занимался этим и в Excel, и в Google'\
                ' Таблицах параллельно, а потом начал преподавать внутри и снаружи. Понял, что мне'\
                ' нравится делать таблицы понятными и доступными.'\
                ' <b>Поэтому я очень хочу, чтобы ты тоже разобрался в сложных темах и работа с'\
                ' таблицами была тебе в кайф!</b>'\
        
        builder.row(types.InlineKeyboardButton(
            text='Посмотреть урок',
            url=self.lk_url)
        )
        builder.row(types.InlineKeyboardButton(
            text='Сдать ДЗ Ренату',
            url=self.lk_url)
        )
        
        await self.bot.bot.send_message(self.tg_user.id, text=msg, reply_markup=builder.as_markup())

    async def lesson_1_6(self):
        builder = InlineKeyboardBuilder()
        msg =   'Видим, что тебе пока не удалось сделать основную домашку. Хотим напомнить, что уже'\
                ' через 59 минут сгорит твоя первая жизнь, если сгорят все жизни, то у тебя закроется доступ'\
                ' к урокам и ты не сможешь получить все подарки, которые мы подготовили для тебя, а именно:'\
                ' \n<i>1) Персональный разбор домашек от Рената</i>'\
                ' \n<i>2) Гайд по горячим клавишам</i>'\
                ' \n<i>3) Гайд по функции XLOOKUP</i>'\
                ' \n<i>4) Все конспекты уроков</i>'\
                ' \n<i>5) 2 видео-урока по использованию нейросетей в работе</i>'\
                ' \n<i>6) скидку до 40% на флагманский курс за выполнение всех домашек</i>'\
                ' \n\n<b>Общая стоимость всех этих бонусов - 60 000 руб, не упусти возможность получить их бесплатно!</b>'
        
        builder.row(types.InlineKeyboardButton(
            text='Выполнить первое задание',
            url=self.lk_url)
        )
        
        await self.photo_message(self.tg_user.id, 'assets/images/presents.png')
        await self.bot.bot.send_message(self.tg_user.id, text=msg, reply_markup=builder.as_markup())
    
    async def lesson_1_7(self):
        builder = InlineKeyboardBuilder()
        msg =   '😓<b>Блин, кажется, у тебя сгорела первая жизнь...'\
                ' Давай сохранимся на этом этапе, посмотрим первый урок и сделаем обязательную'\
                ' домашку, договорились?</b>'\
                ' \n\nК тому же уже в первом уроке мы подготовили для тебя эти темы:'\
                ' \n• Зачем нужны сводные таблицы?'\
                ' \n• Какие данные для сводной подходят, а какие нет?'\
                ' \n• Построение сводной'\
                ' \n• Обновление сводной'\
                ' \n• Источник данных сводной таблицы: диапазоны, столбцы и таблицы'\
                ' \n• Ошибки в данных: как их найти с помощью сводной, как они на сводной отражаются, и как'\
                ' их предотвратить с помощью проверки данных'\
                ' \n• Форматирование в сводной'\
                ' \n• Отличия сводных в Google Spreadsheets и Excel'\
                ' \n\nУже после этого урока ты сможешь строить сводные с нуля или посмотреть на свои'\
                ' текущие таблицы новым взглядом.'\
                ' \n\nИ, конечно, при выполнении основого дз ты заработаешь монеты, которые можно'\
                ' конвертировать в скидку на наш флагманский курс'\
                ' И не забывай о дополнительных монетах за миссии!'\
                ' Ждем тебя в личном кабинете'
        
        builder.row(types.InlineKeyboardButton(
            text='Узнать алгоритм работы со сводными таблицами',
            url=self.lk_url)
        )
        
        await self.photo_message(self.tg_user.id, 'assets/images/lives-1.png')
        await self.bot.bot.send_message(self.tg_user.id, text=msg, reply_markup=builder.as_markup())
    
    async def lesson_1_8(self):
        builder = InlineKeyboardBuilder()
        msg =   '<b>Мы к тебе с тремя аргументами почему лучше не затягивать и посмотреть первый урок прямо сейчас:</b>'\
                ' \n1) Ты сохраняешь возможность забрать все бонусные рубли и все подарки'\
                ' \n<i>2) Ренат ЛИЧНО даёт обратную связь КАЖДОМУ участнику по их домашкам. Не упусти'\
                ' возможность получить разбор от одного из лучших экспертов в РФ, автора и соавтора'\
                ' самых больших Телеграм-каналов по Excel и Google Таблицам в России, автора множества'\
                ' курсов и книг</i>'\
                ' \n3) Ты успеваешь посмотреть урок в комфортном режиме, сделать домашнее задание без'\
                ' спешки, задать вопросы в чате и пообщаться с другими участниками'\
                ' \n\n<b>Убедили? Ждём тебя в личном кабинете, ведь до сгорания второй жизни у тебя'\
                ' осталось всего 1 час 59 минут</b>'
        
        builder.row(types.InlineKeyboardButton(
            text='Иду смотреть',
            url=self.lk_url)
        )
        
        await self.photo_message(self.tg_user.id, 'assets/images/1-5.png')
        await self.bot.bot.send_message(self.tg_user.id, text=msg, reply_markup=builder.as_markup())
    
    async def lesson_1_9(self):
        builder = InlineKeyboardBuilder()
        msg =   '<b>К сожалению, у тебя сгорела ещё одна жизнь</b>😰'\
                ' \nПонимаем, что не всегда быстро удаётся посмотреть уроки, не переживай, у тебя есть ещё'\
                ' целых 12 часов, чтобы всё успеть!'\
                ' \nМы ждём тебя в личном кабинете, в котором ты можешь посмотреть первое видео, сделать'\
                ' обязательное домашнее задание (оно очень простое и доступно к выполнению прямо с'\
                ' телефона), чтобы сохраниться на курсе, а попозже при желании выполнить практическое'\
                ' задание, чтобы попрактиковаться с таблицами и отправить его на разбор Ренату'\
                ' \n\n<b>Двигайся в своем темпе, главное успей выполнить обязательную домашку.'\
                ' \nЕсли что мы всегда рядом!</b>🫂'\
        
        builder.row(types.InlineKeyboardButton(
            text='Сохраниться на курсе',
            url=self.lk_url)
        )
        builder.row(types.InlineKeyboardButton(
            text='Сдать ДЗ',
            url=self.lk_url)
        )
        
        await self.photo_message(self.tg_user.id, 'assets/images/lives-2.png')
        await self.bot.bot.send_message(self.tg_user.id, text=msg, reply_markup=builder.as_markup())

    async def lesson_1_10(self):
        builder = InlineKeyboardBuilder()
        msg =   '<b>Мы знаем как важно быть уверенным в качестве того или иного курса, поэтому'\
                ' хотим поделиться с тобой кейсом студентки нашего флагманского курса по Excel'\
                ' Романенко Екатерины, она работает в сфере логистики</b>'\
                ' \n\nКак видишь, можно знать только базовые функции Excel или Google Таблиц, а в конце'\
                ' нашего курса создавать собственные дашборды и упростить свою работу'\
                ' \n<b>Не упусти возможность получить такой же позитивный опыт как Екатерина, успей'\
                ' выполнить обязательную домашку, чтобы сохраниться на нашем курсе по Сводным таблицам</b>'\
                ' \n\n🔥До сгорания последней жизни осталось 3 часа 59 минут🔥'
        
        builder.row(types.InlineKeyboardButton(
            text='Иду смотреть первый урок',
            url=self.lk_url)
        )
        
        await self.photo_message(self.tg_user.id, 'assets/images/1-6.png')
        await self.bot.bot.send_message(self.tg_user.id, text=msg, reply_markup=builder.as_markup())
    
    async def lesson_1_11(self):
        builder = InlineKeyboardBuilder()
        msg =   'Эх, все твои жизни на нашем курсе по Сводным таблицам сгорели...😭'\
                ' ❌К сожалению, доступ к урокам для тебя закрыт❌'\
                ' Нам очень жаль, что тебе не хватило времени на просмотр первого видео и выполнение'\
                ' задания.'\
                ' Но ты можешь один раз вернуться в программу, если выполнишь задание по кнопке ниже.'\
                ' Если нет времени проходить уроки, но ты точно знаешь, что хочешь прокачаться в работе'\
                ' с Google Таблицами или Excel, просто напиши в личку "Не успеваю смотреть уроки, хочу'\
                ' узнать подробнее про основной курс и получить персональную консультацию"'\
                ' Как тебе идея?'\
                ' <b>Чтобы восстановить доступ пришли в личные сообщения выполненное задание по'\
                ' предыдущему уроку и дождись обратной связи от Рената</b>'\
                ' Или просто напиши: "Не успеваю смотреть уроки, хочу узнать подробнее про курс и'\
                ' получить персональную консультацию"'
        
        builder.row(types.InlineKeyboardButton(
            text='Выполнить задание 1/3',
            url=self.lk_url)
        )
        builder.row(types.InlineKeyboardButton(
            text='Получить персональную консультацию по курсу',
            url=self.lk_url)
        )
        
        await self.photo_message(self.tg_user.id, 'assets/images/lives-3.png')
        await self.bot.bot.send_message(self.tg_user.id, text=msg, reply_markup=builder.as_markup())


        
    
    async def lesson_inactive(self):
        builder = InlineKeyboardBuilder()
        msg =   '<b>Очень жаль, что тебе пришлось закончить своё обучение на этом курсе</b>😓'\
                ' \nУ нас к тебе последняя просьба: пожалуйста, напиши в личку, что тебе помешало/'\
                ' остановило тебя. Мы будем очень благодарны за эту обратную связь, ведь она нам'\
                ' поможет улучшить этот курс и помочь большему количеству людей, желающих'\
                ' разобраться с таблицами🙏'\
                ' \n<b>За обратную связь мы подготовили для тебя подарок: "Гайд по функции XLOOKUP"'\
                ' Отправим его в личке сразу после получения обратной связи</b>'\
                ' \n\nДо встречи!'
        
        builder.row(types.InlineKeyboardButton(
            text='Оставить обратную связь и забрать подарок',
            url=self.lk_url)
        )
        
        await self.photo_message(self.tg_user.id, 'assets/images/inactive.png')
        await self.bot.bot.send_message(self.tg_user.id, text=msg, reply_markup=builder.as_markup())

    async def lesson_done(self):
        builder = InlineKeyboardBuilder()
        msg =   '<b>Задание выполнено! Поздравляем!</b>🎉🥳'\
                ' \n\nНапиши, пожалуйста, небольшой отзыв о просмотренном уроке и обратной связи от'\
                ' Рената, так мы поймём, что именно оказалось для тебя полезным и на чём нам дальше'\
                ' делать акцент, плюс вдохновишь других ребят своим зарядом и настроением!'
        
        builder.row(types.InlineKeyboardButton(
            text='Написать отзыв',
            url=self.lk_url)
        )
        
        await self.photo_message(self.tg_user.id, 'assets/images/done.png')
        await self.bot.bot.send_message(self.tg_user.id, text=msg, reply_markup=builder.as_markup())
    
