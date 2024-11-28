# from test_bot import TgBot
import asyncio
from aiogram import types
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.utils.keyboard import InlineKeyboardBuilder
from logger import logger

class Notifications:

    # def __init__(self, bot: TgBot, tg_user: types.User, lk_url: str):
    def __init__(self, bot, user_id, first_name: str, lk_url: str):
        self.bot = bot
        self.user_id = user_id
        self.first_name = first_name
        self.urls = {
            'lk': lk_url,
            'renat': 'https://t.me/renatshagabutdinov',
            'chat': 'https://t.me/pivottables_bs',
            'yandex': 'https://yandex.ru/maps/org/bonnie_slide/97128190728/?ll=37.672366%2C55.775950&z=14',
            'course': 'https://bonnieandslide.com/kursy/excel-pro?utm_source=telegram&utm_medium=cpc&utm_campaign=250924_B2C_RU_exceltrip&utm_content=doghim_tg&utm_term=sedina-n',
        }
    #     self.session = requests.Session()

    ## UTILITY FUNCTIONS ##

    def read_local_file_id(self, file_name):
            # file_name = "assets/videos/tgvideo"
            file_id = None
            try:
                # Take file_id from txt file if exists
                f = open(file_name + ".txt", "r")
                file_id = f.readline()
                f.close()

            except Exception as e:
                logger.exception(e)
            finally:
                return file_id
            
    def write_local_file_id(self, file_name, file_id):
        try:
            f = open(file_name + ".txt", "w")
            f.write(file_id)
            f.close()

        except Exception as e:
            logger.exception(e)
            
    async def photo_message(self, uid, file_name):
        try:
            file_id = self.read_local_file_id(file_name)
            if (file_id):
                result = await self.bot.bot.send_photo(uid, file_id)
                # print('Reused File ID')
            else:
                photo = types.FSInputFile(file_name)
                result = await self.bot.bot.send_photo(uid, photo)
                file_id = result.photo[0].file_id
                self.write_local_file_id(file_name, file_id)
            # print('File ID: ' + file_id)

        except Exception as e:
            logger.exception(e)

    async def group_message(self, uid, files: list[str]):
        try:
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
                # print(f"File {files[i]} ID: " + file_id)

        except Exception as e:
            logger.exception(e)

    async def video_message(self, uid, file_name):
        try:
            file_id = self.read_local_file_id(file_name)
            if (file_id):
                result = await self.bot.bot.send_video_note(uid, file_id)
                # print('Reused File ID')
            else:
                video = types.FSInputFile(file_name)
                result = await self.bot.bot.send_video_note(uid, video)
                file_id = result.video_note.file_id if result.video_note else result.video.file_id
                self.write_local_file_id(file_name, file_id)
            # print('File ID: ' + file_id)

        except Exception as e:
            logger.exception(e)

    ## LESSON 1 ##

    async def lesson_1_0(self):
        builder = InlineKeyboardBuilder()
        str1 = f'Привет, {self.first_name}!' if self.first_name else 'Привет!'
        msg =   f'{str1} Это Ренат Шагабутдинов и академия Bonnie&Slide.'\
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
            url=self.urls['lk'])
        )
        
        await self.video_message(self.user_id, 'assets/videos/circles/1.mp4')
        await asyncio.sleep(1)
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())
        # return {
        #     'text': msg,
        #     'markup': builder.as_markup()
        # }

    async def lesson_1_1(self):
        builder = InlineKeyboardBuilder()
        msg =   'Мы хотим, чтобы этот курс помог тебе облегчить свою рабочую рутину и пересмотреть'\
                ' свои отношения с таблицами, поэтому очень рады, что ты здесь!'\
                ' \n\n🎁<b>Забирай по кнопке внизу наш первый подарок: гайд "Топ-3'\
                ' механики по ускорению работы с помощью Google Таблиц и Excel на примере'\
                ' реальных кейсов"</b>'
        
        builder.row(types.InlineKeyboardButton(
            text='Забрать гайд',
            url=self.urls['lk'])
        )
        
        photos = [
            'assets/images/1-1.png',
            'assets/images/1-2.png'
        ]
        self.bot.rest.send_mail(self.user_id, 2)
        await self.group_message(self.user_id, photos)
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())

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
            url=self.urls['yandex'])
        )
        
        photos = [
            'assets/images/1-3.png',
            'assets/images/1-4.png'
        ]
        await self.group_message(self.user_id, photos)
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())

    async def lesson_1_3(self):
        builder = InlineKeyboardBuilder()
        str1 = f'<b>{self.first_name}, Excel и Google Таблицы почти всемогущи ведь они:</b>' if self.first_name else 'Excel и Google Таблицы почти всемогущи ведь они:</b>'
        msg =   f'{str1}'\
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
            url=self.urls['lk'])
        )
        
        await self.photo_message(self.user_id, 'assets/images/presents.png')
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())

    async def lesson_1_4(self):
        builder = InlineKeyboardBuilder()
        msg =   '<b>Вернулся к тебе, чтобы напомнить как проходит наш курс-игра по Excel и Google Таблицам</b>✨'\
                ' \n⏰у тебя есть 24 часа на просмотр урока и выполнение ОБЯЗАТЕЛЬНОГО домашнего задания;'\
                ' \n❤️если ты не посмотришь урок и не выполнишь <b>обязательное дз в течение 6 часов, то у тебя сгорит 1-я жизнь,'\
                ' в течение 12 часов - 2-я жизнь, в течение 24 часов - последняя жизнь;</b>'\
                ' \n🙅‍♀️без выполнения <b>основных заданий</b> ты не сможешь продвинуться дальше;'\
                ' \n🪙есть 3 дополнительных (самых простых) задания, за выполнение которых ты также получаешь монеты.'\
                ' <i>Например, прямо сейчас ты можешь стать "Душой компании" - вступай в чат этого курса, представься там и забирай монетку;</i>'\
                ' \n💻также у нас есть практические дз, на которых можно отработать тему урока, но они не обязательны к выполнению.'\
                ' \n\nОтправляй свою основную домашку, пока у тебя не начали сгорать жизни!'
        
        builder.row(types.InlineKeyboardButton(
            text='Посмотреть первый урок',
            url=self.urls['lk'])
        )
        
        await self.video_message(self.user_id, 'assets/videos/circles/2.mp4')
        await asyncio.sleep(1)
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())

    async def lesson_1_5(self):
        builder = InlineKeyboardBuilder()
        msg =   '<b>На связи Ренат, хочу поделиться с тобой, что мне дал навык работы с таблицами</b>📊'\
                ' \n\nЯ работал в крупных компаниях в отделах, занимающихся бюджетированием, и мне'\
                ' нравилось писать макросы и проектировать таблицы так, чтобы многие действия и'\
                ' рутинная работа отдела автоматизировалась, а время тратилось на более сложные'\
                ' интеллектуальные задачи. С приходом в МИФ я занимался этим и в Excel, и в Google'\
                ' Таблицах параллельно, а потом начал преподавать внутри и снаружи. Понял, что мне'\
                ' нравится делать таблицы понятными и доступными.'\
                ' <b>Поэтому я очень хочу, чтобы ты тоже разобрался в сложных темах и работа с'\
                ' таблицами была тебе в кайф!</b>'\
        
        builder.row(types.InlineKeyboardButton(
            text='Посмотреть урок',
            url=self.urls['lk'])
        )
        builder.row(types.InlineKeyboardButton(
            text='Сдать ДЗ Ренату',
            url=self.urls['renat'])
        )
        
        await self.video_message(self.user_id, 'assets/videos/circles/3.mp4')
        await asyncio.sleep(1)
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())

    async def lesson_1_6(self):
        builder = InlineKeyboardBuilder()
        msg =   'Видим, что тебе пока не удалось сделать основную домашку. Хотим напомнить, что уже'\
                ' через 59 минут сгорит твоя первая жизнь, если сгорят все жизни, то у тебя закроется доступ'\
                ' к урокам и ты не сможешь получить все подарки, которые мы подготовили для тебя, а именно:'\
                ' \n<i>1) Персональный разбор домашек от Рената'\
                ' \n2) Гайд по горячим клавишам'\
                ' \n3) Гайд по функции XLOOKUP'\
                ' \n4) Все конспекты уроков'\
                ' \n5) 2 видео-урока по использованию нейросетей в работе'\
                ' \n6) скидку до 40% на флагманский курс за выполнение всех домашек</i>'\
                ' \n\n<b>Общая стоимость всех этих бонусов - 60 000 руб, не упусти возможность получить их бесплатно!</b>'
        
        builder.row(types.InlineKeyboardButton(
            text='Выполнить первое задание',
            url=self.urls['lk'])
        )
        
        await self.photo_message(self.user_id, 'assets/images/presents.png')
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())
    
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
                ' \n\nИ, конечно, при выполнении основного дз ты зарабатываешь монеты, которые можно конвертировать в скидку на наш флагманский курс.'\
                ' Ждём тебя в личном кабинете!'\
                ' \n\n<b>P.S.: не забывай о монетках за дополнительные задания!</b>💰'
        
        builder.row(types.InlineKeyboardButton(
            text='Иду на урок',
            url=self.urls['lk'])
        )
        
        self.bot.rest.set_user_lives(self.user_id, 2)
        await self.photo_message(self.user_id, 'assets/images/lives-1.png')
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())
    
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
                ' остался всего 1 час 59 минут</b>'
        
        builder.row(types.InlineKeyboardButton(
            text='Иду смотреть',
            url=self.urls['lk'])
        )
        
        await self.photo_message(self.user_id, 'assets/images/1-5.png')
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())
    
    async def lesson_1_9(self):
        builder = InlineKeyboardBuilder()
        msg =   '<b>К сожалению, у тебя сгорела ещё одна жизнь</b>😰'\
                ' \nПонимаем, что не всегда быстро удаётся посмотреть уроки, не переживай, у тебя есть ещё'\
                ' целых 12 часов, чтобы всё успеть!'\
                ' \nМы ждём тебя в личном кабинете, в котором ты можешь посмотреть первое видео, сделать'\
                ' обязательное домашнее задание (оно очень простое и доступно к выполнению прямо с'\
                ' телефона), чтобы сохраниться на курсе, а попозже при желании выполнить практическое'\
                ' задание, чтобы поработать с таблицами и получить разбор от Рената'\
                ' \n\n<b>Двигайся в своем темпе, главное успей выполнить обязательную домашку.'\
                ' \nЕсли что мы всегда рядом!</b>🫂'\
        
        builder.row(types.InlineKeyboardButton(
            text='Сохраниться на курсе',
            url=self.urls['lk'])
        )
        builder.row(types.InlineKeyboardButton(
            text='Сдать ДЗ',
            url=self.urls['renat'])
        )
        
        self.bot.rest.set_user_lives(self.user_id, 1)
        await self.photo_message(self.user_id, 'assets/images/lives-2.png')
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())

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
            url=self.urls['lk'])
        )
        
        self.bot.rest.send_mail(self.user_id, 16)
        await self.photo_message(self.user_id, 'assets/images/1-6.png')
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())
    
    async def lesson_1_11(self):
        builder = InlineKeyboardBuilder()
        msg =   'Эх, все твои жизни на нашем курсе по Сводным таблицам сгорели...😭'\
                ' \n\n❌К сожалению, доступ к урокам для тебя закрыт❌'\
                ' \n\nНам очень жаль, что тебе не хватило времени на просмотр первого видео и выполнение'\
                ' задания.'\
                ' Но ты можешь один раз вернуться в программу, если выполнишь задание по кнопке ниже.'\
                ' Если нет времени проходить уроки, но ты точно знаешь, что хочешь прокачаться в работе'\
                ' с Google Таблицами или Excel, просто напиши в личку "Не успеваю смотреть уроки, хочу'\
                ' узнать подробнее про основной курс и получить персональную консультацию"'\
                ' Как тебе идея?'\
                ' \n\n<b>Чтобы восстановить доступ пришли в личные сообщения выполненное задание по'\
                ' предыдущему уроку и дождись обратной связи от Рената</b>'\
                ' Или просто напиши: "Не успеваю смотреть уроки, хочу узнать подробнее про курс и'\
                ' получить персональную консультацию"'
        
        builder.row(types.InlineKeyboardButton(
            text='Выполнить задание 1/3',
            url=self.urls['lk'])
        )
        builder.row(types.InlineKeyboardButton(
            text='Получить персональную консультацию',
            url=self.urls['renat'])
        )
        
        self.bot.rest.set_user_lives(self.user_id, 0)
        self.bot.rest.send_mail(self.user_id, 4)
        await self.photo_message(self.user_id, 'assets/images/lives-3.png')
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())

    async def lesson_1_after_done(self):
        builder = InlineKeyboardBuilder()
        msg =   'Сразу после отзыва переходи к просмотру второго видео-урока!'\
                ' \nВ нём поговорим о настройках макета сводной таблицы, фильтрации, сортировке и'\
                ' группировке, в общем обо всём, что ускоряет работу со сводными.'\
                ' \n<b>Сделаем это на примере данных приложения доставки еды🍔, складских остатков📦'\
                ' и отчёта по продажам</b>'\
        
        builder.row(types.InlineKeyboardButton(
            text='Посмотреть урок',
            url=self.urls['lk'])
        )

        # Wait 1 min before sending
        await asyncio.sleep(60)
        await self.video_message(self.user_id, 'assets/videos/screencasts/2.mp4')
        await asyncio.sleep(1)
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())


    ## LESSON 2 ##
        
    async def lesson_2_0(self):
        builder = InlineKeyboardBuilder()
        msg =   '<b>Почему мы уверены на 100%, что этот мини-курс бустанёт твои навыки и ты не'\
                ' пожалеешь о деньгах и времени, вложенных в него?</b>'\
                ' \nПотому что эксперт курса Ренат Шагабутдинов – преподаватель и консультант по Excel и'\
                ' Google Таблицам с 2012 года, он проводил тренинги в десятках российских компаний.'\
                ' А наша академия Bonnie&Slide обучила более 100 компаний, в числе которых такие'\
                ' гиганты, как Х5, РЖД, Росгосстрах, Билайн, Газпром, Сбер, Pepsi, Nestle, ПСБ и многие другие.'\
                ' \n\n<b>Так что мы очень хорошо понимаем твои потребности и обязательно поможем'\
                ' превратить работу с таблицами в комфортное и интересное времяпрепровождение!</b>'
        
        builder.row(types.InlineKeyboardButton(
            text='Хочу разобраться с таблицами',
            url=self.urls['lk'])
        )
        
        self.bot.rest.send_mail(self.user_id, 5)
        await self.photo_message(self.user_id, 'assets/images/2-1.png')
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())

    # async def lesson_2_1(self):
    #     builder = InlineKeyboardBuilder()
    #     msg =   'На этом курсе мы поставили себе задачу быстро и чётко дать тебе инструменты, благодаря'\
    #             ' которым ты:'\
    #             ' \n📊 научишься строить и обновлять сводные таблицы;'\
    #             ' \n📈 будешь быстрее делать отчёты;'\
    #             ' \n💻 будешь использовать разные формулы и функцию GETPIVOTDATA'\
    #             ' \n\n<b>И всё это уже за 4 урока! Обязательно посмотри 2-й урок, чтобы вдумчиво'\
    #             ' выполнить домашки и получить разбор от Рената</b>'
        
    #     builder.row(types.InlineKeyboardButton(
    #         text='Научиться строить сводные',
    #         url=self.urls['lk'])
    #     )
        
    #     photos = [
    #         'assets/images/2-2.png',
    #         'assets/images/2-3.png',
    #         'assets/images/2-4.png',
    #         'assets/images/2-5.png'
    #     ]
    #     await self.group_message(self.user_id, photos)
    #     await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())

    async def lesson_2_1(self):
        builder = InlineKeyboardBuilder()
        msg =   'Кстати, давно не было кейсов! Хотим поделиться с тобой короткой историей Марины Ерониной, она работает в сфере фармацевтики 💊'\
                ' \n<b>Марина прошла наш флагманский курс и вот, что говорит о своих точках А и Б</b>:'\
                ' \nТочка А: Пришла на курс с базовыми знаниями, был запрос на работу с формулами'\
                ' \nТочка Б: Разобралась с формулами, научилась работать с макросами, очень многое из курса'\
                ' пригодилось в работе'\
                ' \n\n<i>Почти все наши студенты приходят к нам с базовыми знаниями, но по итоге осваивают'\
                ' такие сложные инструменты как составление дашборда, сводные таблицы, макросы, любые'\
                ' вариации формулы ЕСЛИ, прокачиваются в ВПР и т.д.</i>'\
                ' \n\n<b>Уверены, что у тебя тоже всё получится, а фундамент для этого ты закладываешь'\
                ' уже сейчас, на этом курсе</b>🧱'\
                ' \nСмотри новый урок, чтобы закрепить новые знания и двигаться дальше без потери жизни'
        
        builder.row(types.InlineKeyboardButton(
            text='Посмотреть урок',
            url=self.urls['lk'])
        )
        
        await self.photo_message(self.user_id, 'assets/images/2-6.png')
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())

    async def lesson_2_2(self):
        builder = InlineKeyboardBuilder()
        msg =   'С помощью таблиц я автоматизировал всю рутинную работу и высвободил время для'\
                ' задач, которые реально приносят мне удовольствие. Но я понимаю, каково это, когда твой'\
                ' основной рабочий инструмент - таблицы - вызывает кучу вопросов, кажется сложным и'\
                ' скучным.'\
                ' \nПоэтому я здесь, чтобы помочь тебе🫂'\
                ' \nНажимай кнопку ниже и смотри новый урок'
        
        builder.row(types.InlineKeyboardButton(
            text='Разобраться с таблицами',
            url=self.urls['lk'])
        )
        
        await self.video_message(self.user_id, 'assets/videos/circles/4.mp4')
        await asyncio.sleep(1)
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())

    # async def lesson_2_4(self):
    #     builder = InlineKeyboardBuilder()
    #     msg =   'Я практик и всё, что мы даём на этом курсе - результат моей работы в крупных компаниях,'\
    #             ' работы в издательстве МИФ и многих лет преподавания, а также экспертиза Bonnie&Slide,'\
    #             ' которые более 9 лет помогают сотрудникам корпораций ускорять работу с отчётами.'\
    #             ' \n\n<b>Поэтому разборы домашних заданий я провожу лично, так как хочу помочь'\
    #             ' каждому персонально пройти из точки А, в которой ничего не понятно и ты тратишь'\
    #             ' 100 часов на один отчет, в точку Б, в которой у тебя будет четкая структура работы в'\
    #             ' таблицах и половина задач автоматизируется</b>🚀'\
    #             ' \n\nЖду тебя на разбор!'
        
    #     builder.row(types.InlineKeyboardButton(
    #         text='Посмотреть урок и сдать дз',
    #         url=self.urls['lk'])
    #     )
        
    #     await self.video_message(self.user_id, 'assets/videos/circles/5.mp4')
    #     await asyncio.sleep(1)
    #     await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())

    async def lesson_2_3(self):
        builder = InlineKeyboardBuilder()
        msg =   'Чтобы работа со сводными таблицами и формулами действительно упрощала работу,'\
                ' нужно👇'\
                ' \n<i>1) автоматизировать выгрузку данных в таблицы;'\
                ' \n2) использовать умные фильтры;'\
                ' \n3) получить пошаговый план по тому, КАКИЕ именно действия предпринимать, чтобы не'\
                ' путаться и не паниковать при работе с таблицами;'\
                ' \n4) практиковаться и получать подробные разборы ошибок</i>'\
                ' \n\n<b>Всё это мы даём на нашем мини-курсе❤️</b>'\
                ' \n\nИ просто посмотри, что можно делать на основе сводных👆 до: большая таблица,'\
                ' в которой с первого взгляда сложно что-то понять, а после: понятная визуалиазация,'\
                ' потому что на основе сводных можно делать вот такие небольшие дашборды для своих отчётов.'\
                ' \n\nЗа эту универсальность мы и любим сводные, так что продолжай смотреть уроки, чтобы освоить их'\
                ' на максимум и понять потенциал этого инструмента! (P.S.: 🔥до сгорания первой жизни осталось 29 минут🔥)'
                
        
        builder.row(types.InlineKeyboardButton(
            text='Сдать дз Ренату',
            url=self.urls['renat'])
        )
        
        photos = [
            'assets/images/2-7.png',
            'assets/images/2-8.png'
        ]
        await self.group_message(self.user_id, photos)
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())

    async def lesson_2_4(self):
        builder = InlineKeyboardBuilder()
        msg =   '<b>Внимание! У тебя сгорела 1 жизнь, так как мы пока не получили твоё основное'\
                ' домашнее задание</b>😓'\
                ' \n\nЕсли у тебя сгорят все 3 жизни, то ты потеряешь доступ к урокам, обратной связи от Рената'\
                ' и бонусам на 60 000 руб...'\
                ' \n\nУ тебя осталось 5 часов 59 минут, чтобы выполнить домашнее задание без потери ещё'\
                ' одной жизни'\
                ' \n\n<b>Прямо сейчас переходи в личный кабинет и выполни обязательное дз</b>'
        
        builder.row(types.InlineKeyboardButton(
            text='Сохранить жизни',
            url=self.urls['lk'])
        )
        
        self.bot.rest.set_user_lives(self.user_id, 2)
        await self.photo_message(self.user_id, 'assets/images/lives-1.png')
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())

    async def lesson_2_5(self):
        builder = InlineKeyboardBuilder()
        msg =   '🎁<b>Хотим тебе напомнить, что же входит в бонусы на 60 000 рублей, которые ты'\
                ' можешь получить на этом курсе</b>🎁'\
                ' \n\n1) Гайд Топ-3 механики по ускорению работы с помощью Google Таблиц и Excel на примере'\
                ' реальных кейсов, который ждал тебя на старте курса'\
                ' \n2) Гайд по горячим клавишам'\
                ' \n3) Гайд по функции XLOOKUP'\
                ' \n4) Все конспекты уроков'\
                ' \n5) 2 видео-урока по использованию нейросетей в работе'\
                ' \n6) скидка до 40 % на флагманский курс за выполнение основных и дополнительных'\
                ' домашек'\
                ' \n\n<b>Продолжай собирать монеты и ты сможешь конвертировать их в скидку на покупку'\
                ' нашего флагманского курса</b>🪙'\
                ' \n\nТак что не упусти возможность забрать все подарки, успей выполнить домашку, чтобы'\
                ' сохранить жизни и продолжать проходить курс'\
                ' \n🔥<b>До сгорания второй жизни осталось 2 часа 59 минут</b>🔥'
        
        builder.row(types.InlineKeyboardButton(
            text='Сохранить за собой все подарки',
            url=self.urls['lk'])
        )
        
        await self.photo_message(self.user_id, 'assets/images/presents.png')
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())

    async def lesson_2_6(self):
        builder = InlineKeyboardBuilder()
        msg =   '<b>Нам жаль, но у тебя сгорела вторая жизнь, тк основное домашнее задание ещё не'\
                ' выполнено...</b> 😰'\
                ' \nЧерез 12 часов сгорит последняя жизнь, и тогда доступ к урокам, обратной связи от Рената'\
                ' и бонусам на 60 000 рублей закроется'\
                ' \n\nРекомендуем прямо сейчас перейти в личный кабинет и выполнить текущее основное'\
                ' задание'
        
        builder.row(types.InlineKeyboardButton(
            text='Выполнить задание 2/3',
            url=self.urls['lk'])
        )
        
        self.bot.rest.set_user_lives(self.user_id, 1)
        await self.photo_message(self.user_id, 'assets/images/lives-2.png')
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())

    async def lesson_2_7(self):
        builder = InlineKeyboardBuilder()
        msg =   '<b>Через 5 часов 59 минут у тебя сгорит последняя жизнь и ты потеряешь доступ к'\
                ' нашему курсу</b>❌'\
                ' \nЧтобы продолжать смотреть уроки, ты можешь выполнить только обязательное задание,'\
                ' если у тебя не хватает времени выполнять все домашки.'\
                ' \n\n<i>Мы понимаем, что сложно успевать всё, но хотим, чтобы ты посмотрел все уроки и смог'\
                ' получить подарки на 60 000 рублей в конце курса</i>🎁'\
                ' \n\nПросто перейди в личный кабинет и сделай обязательное домашнее задание, чтобы'\
                ' сохраниться на курсе и продолжить обучение работе со сводными таблицами'
        
        builder.row(types.InlineKeyboardButton(
            text='Бегу смотреть',
            url=self.urls['lk'])
        )
        
        await self.video_message(self.user_id, 'assets/videos/circles/6.mp4')
        await asyncio.sleep(1)
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())

    async def lesson_2_8(self):
        builder = InlineKeyboardBuilder()
        msg =   '<b>Пока мы не получили твоё обязательное дз, хотим познакомить тебя с Ольгой'\
                ' Власовой.</b>'\
                ' \n\nКак видишь, наши студенты работают в разных сферах: банки, логистика, продажи,'\
                ' страхование и тд, но все они получили то, что упростило и ускорило их работу с таблицами.'\
                ' \n<b>Хочешь так же?</b>'\
                ' \n<i>У тебя осталось 2 часа 59 минут, чтобы сохраниться на курсе и уже сейчас сделать сводные'\
                ' таблицы самой простой частью своей работы</i>📑'
        
        builder.row(types.InlineKeyboardButton(
            text='Хочу как Ольга',
            url=self.urls['lk'])
        )
        
        self.bot.rest.send_mail(self.user_id, 13)
        await self.photo_message(self.user_id, 'assets/images/2-9.png')
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())

    async def lesson_2_9(self):
        builder = InlineKeyboardBuilder()
        msg =   '<b>Эх, все твои жизни на нашем курсе по Сводным таблицам сгорели...😭'\
                ' ❌К сожалению, доступ к урокам для тебя закрыт</b>❌'\
                ' \n\nНам очень жаль, что тебе не хватило времени на просмотр урока и выполнение задания.'\
                ' Но ты можешь вернуться в программу, если выполнишь задание по кнопке ниже.'\
                ' Если нет времени проходить уроки, но ты точно знаешь, что хочешь прокачаться в работе'\
                ' с Google Таблицами или Excel, просто напиши в личку "Не успеваю смотреть уроки, хочу'\
                ' узнать подробнее про основной курс и получить персональную консультацию"'\
                ' \n\n<b>Чтобы восстановить доступ пришли в личные сообщения выполненное задание по'\
                ' предыдущему уроку и дождись обратной связи от Рената'\
                ' Или напиши: "Не успеваю смотреть уроки, хочу узнать подробнее про курс и'\
                ' получить персональную консультацию"</b>'
        
        builder.row(types.InlineKeyboardButton(
            text='Выполнить задание 2/3',
            url=self.urls['lk'])
        )
        builder.row(types.InlineKeyboardButton(
            text='Получить персональную консультацию по курсу',
            url=self.urls['renat'])
        )
        
        self.bot.rest.set_user_lives(self.user_id, 0)
        self.bot.rest.send_mail(self.user_id, 7)
        await self.photo_message(self.user_id, 'assets/images/lives-3.png')
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())

    
    ## LESSON 3 ##

    async def lesson_3_0(self):
        builder = InlineKeyboardBuilder()
        msg =   '<b>Мы перешли через экватор нашего курса</b>🚀'\
                ' \nОсталось ещё 2 мощных урока, сегодня мы переходим к <b>уроку 3: "Вычисления: разные'\
                ' функции в области значений. Доли"</b>'\
                ' \nБудем активно считать, как раз то, что нужно для твоих отчётов.'\
                ' \n\nСегодня ты научишься:'\
                ' \n• менять вычисление в области значений сводной (сумма, количество, среднее и другие функции)'\
                ' \n• вычислять несколькими способами по одному и тому же полю, например, сумма и среднее продаж'\
                ' \n• считать уникальные значения: сколько наименований покупал каждый клиент,'\
                ' \n• сколько товаров (<u>не единиц, а наименований!</u>) хранится в каждом городе'\
                ' \n• считать доли в сводной: по строкам, столбцам и в целом'\
                ' \n\n<b>Всё это, конечно, сможешь закрепить на практике с помощью домашнего задания и'\
                ' получить персональный разбор от Рената!</b>'\
                ' \n\nЖдём тебя в личном кабинете'
        
        builder.row(types.InlineKeyboardButton(
            text='Смотреть 3й урок',
            url=self.urls['lk'])
        )
        
        self.bot.rest.send_mail(self.user_id, 8)
        await self.video_message(self.user_id, 'assets/videos/screencasts/3.mov')
        await asyncio.sleep(1)
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())

    async def lesson_3_1(self):
        builder = InlineKeyboardBuilder()
        msg =   '<b>Вчера мы получили такой вопрос от одного из участников этого мини-курса:</b>'\
                ' \n<i>"Мне пока вроде бы всё понятно, спасибо, что сделали подробный разбор домашек. Но в'\
                ' целом у меня очень базовые познания в экселе, мне есть смысл дальше рассматривать'\
                ' покупку вашего основного курса или он только для продвинутых пользователей? Хочу'\
                ' научиться большему, чем просто сводным, но не знаю справлюсь ли"</i>'\
                ' \n\nДавай ответим примером нашей студентки Надежды Казимиренко 👆'\
                ' \n\n<b>То есть смотри, точка А Надежды - базовые знания; точка Б - горячие клавиши,'\
                ' прокачка знаний, понимание как работают сложные формулы.</b>'\
                ' \nТебе не обязательно быть продвинутым пользователем Excel, чтобы учиться на наших'\
                ' флагманских курсах, ведь у нас есть отдельные программы для новичков и для более'\
                ' опытных.'\
                ' \nПоэтому можешь спокойно проходить наш мини-курс, зная, что в конце ты сможешь'\
                ' подобрать для себя идеальную программу и формат❤️'
        
        builder.row(types.InlineKeyboardButton(
            text='Продолжить изучение сводных таблиц',
            url=self.urls['lk'])
        )
        
        await self.photo_message(self.user_id, 'assets/images/3-1.png')
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())

    # async def lesson_3_2(self):
    #     builder = InlineKeyboardBuilder()
    #     msg =   'Для нашего мини-курса мы неспроста выбрали тему, которая за 4 урока улучшит твою'\
    #             ' работу с таблицами х3 - Сводные таблицы.'\
    #             ' \nСводные таблицы сводят с ума, тех кто так и не научился с ними работать и пугают тех, кто'\
    #             ' только хочет начать ими пользоваться.'\
    #             ' \n<b>На курсе мы составили уроки таким образом, чтобы плавно прокачать твои навыки'\
    #             ' аналитики, планирования и прогнозирования, чтобы сразу после курса тебе удалось'\
    #             ' облегчить работу с отчетами. Особенно подробным и полезным получился 3-й урок</b>'\
    #             ' \n\nА после каждого урока у нас есть задания непосредственно в таблицах для тех, кто хочет'\
    #             ' закреплять информацию, пройденную на уроках, и получать разборы от Рената.'\
    #             ' \n\n<i>Ждём твою третью основную домашку, уже совсем скоро финал курса и много приятных'\
    #             ' подарков!</i>'
        
    #     builder.row(types.InlineKeyboardButton(
    #         text='Посмотреть урок 3/4',
    #         url=self.urls['lk'])
    #     )
        
    #     await self.photo_message(self.user_id, 'assets/images/2-4.png') # 2-4 is correct
    #     await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())

    async def lesson_3_2(self):
        builder = InlineKeyboardBuilder()
        msg =   'Когда я пришел в издательство МИФ и начал работать над своей книгой (тираж 5,5 тыс'\
                ' экземпляров менее, чем за год), я понял, что вокруг темы таблиц много хороших'\
                ' преподавателей, много интересных тем, много людей, желающих научиться работе с ними,'\
                ' но также много предубеждений, что таблицы это скучно и не реально сложно.'\
                ' Именно поэтому я поставил себе задачу максимально упростить и сделать интересным'\
                ' преподавание этой темы.'\
                ' \n\n📊<b>По этой причине на нашем мини-курсе мы разбираем тему Сводных таблиц не на'\
                ' оторванных от реальности примерах, а на примерах доставок еды, складских'\
                ' остатков, отчетов по сделкам в отделе продаж, отчетов HR.'\
                ' Чтобы этот курс был максимально приближен к твоим рабочим задачам.</b>'\
                ' \n\nТак что скорее смотри новый урок, а, если урок уже просмотрен, то я жду тебя в личке с'\
                ' новой домашкой'
        
        builder.row(types.InlineKeyboardButton(
            text='Посмотреть новый урок',
            url=self.urls['lk'])
        )
        builder.row(types.InlineKeyboardButton(
            text='Сдать домашку Ренату на разбор',
            url=self.urls['renat'])
        )
        
        await self.video_message(self.user_id, 'assets/videos/circles/7.mp4')
        await asyncio.sleep(1)
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())

    # async def lesson_3_4(self):
    #     builder = InlineKeyboardBuilder()
    #     msg =   'Вся наша команда знает, что покупать курсы хочется у тех, кому можно доверять, кто давно'\
    #             ' существует на рынке и кто точно сможет помочь и поддержать, когда что-то не получается.'\
    #             ' \n\nУже сейчас нам поступают вопросы о наших флагманских курсах, но прежде, чем говорить'\
    #             ' о них, мы хотим поделиться честным мнением наших студентов, которые уже были на'\
    #             ' твоём месте и проходили наши курсы по Excel.'\
    #             ' \n<b>Мы гордимся каждым нашим студентов, ведь позитивный итог это, в первую'\
    #             ' очередь, заслуга их трудолюбия и заинтересованности, а мы только рады стать'\
    #             ' надёжным плечом на этом пути</b>🙌'
        
    #     builder.row(types.InlineKeyboardButton(
    #         text='Хочу так же, иду смотреть урок 3/4',
    #         url=self.urls['lk'])
    #     )
        
    #     photos = [
    #         'assets/images/3-2.png',
    #         'assets/images/3-3.png'
    #     ]
    #     await self.group_message(self.user_id, photos)
    #     await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())
    #     self.bot.rest.send_mail(self.user_id, 20)

    async def lesson_3_3(self):
        builder = InlineKeyboardBuilder()
        msg =   '<b>Почему тебе стоит дойти до конца этого курса?</b>🤔'\
                ' \nРенат, автор этого курса, практик и человек, который не только сам ежедневно использует'\
                ' таблицы в своей работе, но и обучил уже более 2000 человек этому навыку.'\
                ' \nМы, академия Bonnie&Slide, тоже практики, компания, которая выпустила уже более 80 000'\
                ' студентов, среди которых сотрудники таких компаний как Х5, Теле2, Билайн, РЖД, Газпром'\
                ' и тд, ежедневно работающие с графиками, таблицами, отчётами.'\
                ' \n\nМы вложили в этот курс практические задания на понятных кейсах службы доставки,'\
                ' складских остатков, отчетов отдела продаж, чтобы у тебя была возможность набивать руку'\
                ' и к концу курса тебе стала понятна механика работы со сводными таблицами.'\
                ' \n\n👇<b>В конце этого курса ты научишься👇'\
                ' \n01 Строить, обновлять, форматировать сводные таблицы в несколько кликов'\
                ' \n02 Настраивать макет сводной таблицы, использовать группировку, фильтры и срезы'\
                ' \n03 Делать вычисления с помощью разных функций, считать доли'\
                ' \n04 Использовать разные формулы и функцию GETPIVOTDATA</b>'\
                ' \n\nНе упускай классную возможность прокачаться и успей посмотреть урок и сдать хотя бы'\
                ' обязательную домашку'\
                ' ⏱️<i>У тебя осталось 59 минут, чтобы сохранить все свои жизни</i>'
        
        builder.row(types.InlineKeyboardButton(
            text='Посмотреть урок 3/4',
            url=self.urls['lk'])
        )
        builder.row(types.InlineKeyboardButton(
            text='Сдать дз Ренату',
            url=self.urls['renat'])
        )
        
        photos = [
            'assets/images/3-4.png',
            'assets/images/3-5.png'
        ]
        await self.group_message(self.user_id, photos)
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())
        
    async def lesson_3_4(self):
        builder = InlineKeyboardBuilder()
        msg =   '<b>Внимание! У тебя сгорела 1 жизнь, так как мы пока не получили твоё основное'\
                ' домашнее задание</b>💔'\
                ' \n\nЕсли у тебя сгорят все 3 жизни, то ты потеряешь доступ к урокам, обратной связи от Рената'\
                ' и бонусам на 60 000 руб...'\
                ' \n\nУ тебя осталось 5 часов 59 минут, чтобы выполнить домашнее задание без потери ещё'\
                ' одной жизни'\
                ' \n\n<b>Прямо сейчас переходи в личный кабинет и выполни обязательное дз</b>'
        
        builder.row(types.InlineKeyboardButton(
            text='Сохранить жизни',
            url=self.urls['lk'])
        )
        
        self.bot.rest.set_user_lives(self.user_id, 2)
        await self.photo_message(self.user_id, 'assets/images/lives-1.png')
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())

    async def lesson_3_5(self):
        builder = InlineKeyboardBuilder()
        msg =   'Напомним, что на нашем курсе ты можешь выполнять дополнительные домашки и'\
                ' получать достижения, которые позже можно конвертировать в скидку на флагманский курс.'\
                ' \nТы можешь стать "Душой компани", "Лучшим другом" и "Телеграм-бро"'\
                ' \n<b>Подробнее о заданиях читай в личном кабинете</b>'\
                ' \n\n<i>P.S.: если тебе еще не удалось сдать домашку, то у тебя осталось 2 часа 59 минут до'\
                ' сгорания второй жизни...</i>💔'
        
        builder.row(types.InlineKeyboardButton(
            text='Выполнить доп. задание',
            url=self.urls['lk'])
        )        
        builder.row(types.InlineKeyboardButton(
            text='Продолжить смотреть уроки',
            url=self.urls['lk'])
        )
        
        photos = [
            'assets/images/achiv-1.jpg',
            'assets/images/achiv-2.jpg',
            'assets/images/achiv-3.jpg'
        ]
        await self.group_message(self.user_id, photos)
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())
        
    async def lesson_3_6(self):
        builder = InlineKeyboardBuilder()
        msg =   '<b>Нам жаль, но у тебя сгорела вторая жизнь, тк основное домашнее задание ещё не'\
                ' выполнено...</b> 😰'\
                ' \nЧерез 12 часов сгорит последняя жизнь, и тогда доступ к урокам, обратной связи от Рената'\
                ' и бонусам на 60 000 рублей закроется'\
                ' \n\nРекомендуем прямо сейчас перейти в личный кабинет и выполнить текущее основное'\
                ' задание'
        
        builder.row(types.InlineKeyboardButton(
            text='Выполнить задание 3/4',
            url=self.urls['lk'])
        )
        
        self.bot.rest.set_user_lives(self.user_id, 1)
        await self.photo_message(self.user_id, 'assets/images/lives-2.png')
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())

    async def lesson_3_7(self):
        builder = InlineKeyboardBuilder()
        msg =   'Через 5 часов 59 минут у тебя сгорит последняя жизнь и ты потеряешь доступ к нашему'\
                ' курсу❤️❌'\
                ' \n<b>Чтобы продолжать смотреть уроки, ты можешь выполнить только обязательное'\
                ' задание к 3-му уроку, если у тебя не хватает времени выполнять все домашки</b>'\
                ' \n\nМы понимаем, что сложно успевать всё, но хотим, чтобы ты посмотрел все уроки и смог'\
                ' получить подарки на 60 000 рублей в конце курса🎁'\
                ' \n\n<i>Просто перейди в личный кабинет и сделай обязательное домашнее задание, чтобы'\
                ' сохраниться на курсе и продолжить обучение работе со сводными таблицами</i>'
        
        builder.row(types.InlineKeyboardButton(
            text='Бегу смотреть',
            url=self.urls['lk'])
        )
        
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())

    async def lesson_3_8(self):
        builder = InlineKeyboardBuilder()
        msg =   '<b>Эх, все твои жизни на нашем курсе по Сводным таблицам сгорели...😭'\
                ' \n❌К сожалению, доступ к урокам для тебя закрыт</b>❌'\
                ' \n\nНам очень жаль, что тебе не хватило времени на просмотр урока и выполнение задания.'\
                ' Но ты можешь вернуться в программу, если выполнишь задание по кнопке ниже.'\
                ' Если нет времени проходить уроки, но ты точно знаешь, что хочешь прокачаться в работе'\
                ' с Google Таблицами или Excel, просто напиши в личку "Не успеваю смотреть уроки, хочу'\
                ' узнать подробнее про основной курс и получить персональную консультацию"'\
                ' \n\n<b>Чтобы восстановить доступ пришли в личные сообщения выполненное задание по'\
                ' предыдущему уроку и дождись обратной связи от Рената'\
                ' Или напиши: "Не успеваю смотреть уроки, хочу узнать подробнее про курс и'\
                ' получить персональную консультацию"</b>'
        
        builder.row(types.InlineKeyboardButton(
            text='Выполнить задание 3/4',
            url=self.urls['lk'])
        )
        builder.row(types.InlineKeyboardButton(
            text='Получить персональную консультацию',
            url=self.urls['renat'])
        )
        
        self.bot.rest.set_user_lives(self.user_id, 0)
        self.bot.rest.send_mail(self.user_id, 10)
        await self.photo_message(self.user_id, 'assets/images/lives-3.png')
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())

    
    ## LESSON 4 ##

    async def lesson_4_0(self):
        builder = InlineKeyboardBuilder()
        msg =   '<b>Ну что! Финишная прямая! Вау!</b>🏁'\
                ' \nТебе покорились уже три урока и три домашки, остался последний урок из нашего курса -'\
                ' <i>Сводная таблица на основе нескольких источников данных</i>'\
                ' \n\nВ этом видео-уроке Ренат покажет как собрать данные и построить сводную из нескольких'\
                ' таблиц (с разных листов в одном файле или из разных файлов)'\
                ' \n\nИ уже после этого урока ты наконец-то сможешь забрать все обещанные подарки!'\
                ' \nМы уже в предвкушении финала, а ты?🥰'
        
        builder.row(types.InlineKeyboardButton(
            text='Иду смотреть финальный урок и забирать подарки',
            url=self.urls['lk'])
        )
        
        self.bot.rest.send_mail(self.user_id, 11)
        await self.video_message(self.user_id, 'assets/videos/screencasts/4.mov')
        await asyncio.sleep(1)
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())

    async def lesson_4_1(self):
        builder = InlineKeyboardBuilder()
        msg =   'Я надеюсь, тебе уже удалось посмотреть наш финальный урок! После у него у нас нет'\
                ' домашки, но у меня к тебе есть просьба:'\
                ' <b>напиши мне в личку как ты? как тебе такой 4х'\
                ' дневный формат? были ли полезны уроки? что понравилось, что не очень, что'\
                ' получилось, а с чем еще нужна помощь?</b>🤲'\
                ' \nВ общем, поделись своими мыслями, я буду очень благодарен тебе! Я постарался сделать'\
                ' наши уроки максимально понятными и мне важно понять удалось ли мне задуманное!'\
                ' \n\nА если посмотреть урок еще не было времени, то переходи по кнопке ниже и смотри'\
                ' скорее! Там тебя ждёт и последний урок, и подарки, и самые классные новости по'\
                ' флагманскому курсу от Bonnie&Slide! 🤩'
        
        builder.row(types.InlineKeyboardButton(
            text='Бегу смотреть',
            url=self.urls['lk'])
        )
        builder.row(types.InlineKeyboardButton(
            text='Написать Ренату',
            url=self.urls['renat'])
        )
        
        self.bot.rest.send_mail(self.user_id, 12)
        await self.video_message(self.user_id, 'assets/videos/circles/8.mp4')
        await asyncio.sleep(1)
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())

    async def lesson_4_2(self):
        builder = InlineKeyboardBuilder()
        msg =   'Этот мини-курс лишь часть всего того, что мы даём на наших флагманских курсах по Excel и'\
                ' Google таблицах на базовом и продвинутом уровнях.'\
                ' \n<b>Там мы разбираем всё от формул СЧЁТ, СУММ и функций ЕСЛИ, СУММЕСЛИ, ЧАСТНОЕ,'\
                ' умных таблиц, макросов до настройки дашбордов, диаграммы Ганта и работы с'\
                ' умной ВПР.</b>'\
                ' \nОдин из наших студентов Дмитрий Демьянов делится👆'\
                ' "Я пришел на курс с минимальным набором навыков: vlookup, pivot, а закончил его с'\
                ' улучшением текущих умений, новыми взглядами и подходами в обработке информации и'\
                ' сведении данных в читабельный вид. Узнал новые формулы"'\
                ' \n\nТы можешь также как Дмитрий решить свои задачи и войти в число наших студентов,'\
                ' рабочая рутина которых облегчилась благодаря инструментам Excel и Google Таблиц!'\
                ' \n\n<b>У тебя есть 24 часа, чтобы оставить заявку на наш флагманский курс, сохранив'\
                ' возможность получить скидку за счёт бонусных рублей, которые тебе удалось'\
                ' накопить!</b>'
        
        builder.row(types.InlineKeyboardButton(
            text='Хочу так же как Дмитрий',
            url='https://bonnieandslide.com/kursy/excel-pro')
        )
        
        await self.photo_message(self.user_id, 'assets/images/4-1.png')
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())

    async def lesson_4_3(self):
        builder = InlineKeyboardBuilder()
        msg =   'Наша студентка Вероника Некрасова работает в сфере управления персоналом и вот, что'\
                ' говорит о нашем курсе по Excel👆'\
                ' \n"Я пришла на курс с базовыми знаниями, умела пользоваться формулами и ВПР, а теперь'\
                ' из моих скучных отчётов я могу делать понятные и удобные дашборды"'\
                ' \n\nКак видишь, наши студенты работают в абсолютно разных сферах, но все они находят'\
                ' полезные для себя инструменты.'\
                ' \n<b>Ты можешь также!</b>🚀'
        
        builder.row(types.InlineKeyboardButton(
            text='Хочу узнать подробнее',
            url=self.urls['lk'])
        )
        
        await self.photo_message(self.user_id, 'assets/images/4-2.png')
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())

    async def lesson_4_4(self):
        builder = InlineKeyboardBuilder()
        msg =   'Тебе удалось накопить много монет, мы гордимся тобой!💰'\
                ' \n<b>Это значит, что ты можешь потратить их на покупку одного из тарифов нашего'\
                ' флагманского курса по Excel. И, конечно, не забудь получить все подарки, к которым'\
                ' ты шёл на протяжении этого курса</b>'\
                ' \n\nСмотри финальный урок с Ренатом, а, если хочешь подробнее узнать о флагманском курсе,'\
                ' то на персональной консультации куратор этого направления ответит на все твои вопросы!'\
                ' \n\n<i>Успевай воспользоваться своими бонусами, которые собирались таким трудом, тк они'\
                ' сгорят уже через 16 часов</i>🔥'
        
        builder.row(types.InlineKeyboardButton(
            text='Посмотреть урок 4/4',
            url=self.urls['lk'])
        )
        builder.row(types.InlineKeyboardButton(
            text='Получить персональную консультацию',
            url=self.urls['renat'])
        )
        
        self.bot.rest.send_mail(self.user_id, 18)
        await self.photo_message(self.user_id, 'assets/images/4-3.png')
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())

    async def lesson_4_5(self):
        builder = InlineKeyboardBuilder()
        msg =   '<b>У тебя осталось 12 часов на то, чтобы сохранить за собой самые выгодные условия'\
                ' приобретения основного курса</b>✨'\
                ' \nЗа время мини-курса ты мог выполнить все 6 домашек и накопить максимальное'\
                ' количество монет, которые в сумме составляют скидку 30% + мы дарим дополнительную'\
                ' скидку 10%, таким образом просто посмотри, какая получается экономия 🔥'\
                ' \n\n<b>ВАЖНО: дополнительная скидка 10% держится 30 минут после просмотра финального урока,'\
                ' а твоя накопленная скидка держится 24 часа</b> ⏱️'\
                ' \n\nЕсли у тебя есть вопросы, ты можешь написать в личку Ренату, и он поможет тебе'
        
        builder.row(types.InlineKeyboardButton(
            text='Воспользоваться скидкой',
            url=self.urls['lk'])
        )
        
        await self.photo_message(self.user_id, 'assets/images/4-4.png')
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())
    
    # async def lesson_4_6(self):
    #     builder = InlineKeyboardBuilder()
    #     msg =   'Давай расскажем подробнее о программе курса по Excel и Google Таблицам, чтобы тебе'\
    #             ' было понятно, чего от нас ждать👆'\
    #             ' \nУ нас есть два курса: один базовый, а второй продвинутый, поэтому идеальный формат'\
    #             ' обучения мы сможем подобрать для каждого!'\
    #             ' \n\n<b>Смотри финальный урок нашего мини-курса, на котором мы строим сводную из'\
    #             ' нескольких источников данных, актуализируем информацию и автоматизируем'\
    #             ' обновления</b>📊'\
    #             ' \n\n<i>Но помни, что на флагманском курсе всего 80 мест, 21 из них уже занято</i>'
        
    #     builder.row(types.InlineKeyboardButton(
    #         text='Посмотреть финальный урок',
    #         url=self.urls['lk'])
    #     )
    #     builder.row(types.InlineKeyboardButton(
    #         text='Забронировать место на курсе',
    #         url=self.urls['lk'])
    #     )
        
    #     photos = [
    #         'assets/images/4-5.png',
    #         'assets/images/4-6.png',
    #         'assets/images/4-7.png',
    #         'assets/images/4-8.png'
    #     ]
    #     await self.group_message(self.user_id, photos)
    #     await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())
    
    # async def lesson_4_7(self):
    #     builder = InlineKeyboardBuilder()
    #     msg =   '❌<b>Через 3 часа 59 минут ты потеряешь возможность занять место на курсе по самой'\
    #             ' выгодной цене</b>❌'\
    #             ' \n\n<u>Но у нас есть важное объявление: мы закрепили для тебя МАКСИМАЛЬНУЮ СКИДКУ,'\
    #             ' то есть за тобой сохранилась не только накопленная скидка, но и те 10%, о которых мы говорили в финальном уроке!</u>'\
    #             ' \n\n<i>Если ты хочешь прокачать свои навыки, узнать новые формулы, научиться работать с'\
    #             ' макросами, дашбордами, автоматизировать рутинные задачи и высвободить время для'\
    #             ' более интеллектуальных или интересных задач, то оставляй заявку на наш курс и сохраняй'\
    #             ' место за собой по лучшей цене.</i>'\
    #             ' \n\nНа курсе всего 80 мест, из них занята уже половина'
        
    #     builder.row(types.InlineKeyboardButton(
    #         text='Хочу на курс',
    #         url=self.urls['lk'])
    #     )

    #     await self.photo_message(self.user_id, 'assets/images/4-9.png')
    #     await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())
    #     self.bot.rest.send_mail(self.user_id, 21)
    
    async def lesson_4_6(self):
        builder = InlineKeyboardBuilder()
        msg =   'Ты уже сделал первый шаг, освоив базовые навыки работы со сводными таблицами, но это'\
                ' <i>только вершина айсберга</i>'\
                ' \n<b><i>Те знания, которые ты можешь получить, могут кардинально изменить твою карьеру'\
                ' и подход к работе с данными.</i></b>'\
                ' \n\nДавай заглянем в будущее и посмотрим, какие достижения могут стать твоей'\
                ' реальностью?🔮'\
                ' \n🚀 <b>Карьерный рост и новые возможности</b>'\
                ' \nПо данным LinkedIn, навыки работы с Excel входят в топ-10 наиболее востребованных'\
                ' у работодателей по всему миру'\
                ' \n💪🏻 <b>Сокращение времени на подготовку отчетов с нескольких часов до нескольких минут</b>'\
                ' \nНапример, наши студенты из отдела продаж смогли оптимизировать свои процессы,'\
                ' используя продвинутые функции сводных таблиц и макросов. Это не просто ускорило их'\
                ' работу, но и позволило им анализировать данные более глубоко, что привело к росту продаж'\
                ' \n💸 <b>Возможность вырасти в доходе</b>'\
                ' \nПомимо того, что умение пользоваться таблицами на высоком уровне часто становится'\
                ' критически важным для продвижения по карьерной лестнице, этот навык ещё можно'\
                ' монетизировать в виде дополнительного заработка.'\
                ' <i>На hh.ru больше 35 000 вакансий, по'\
                ' которым ищут специалистов по работе с таблицами</i>'\
                ' \n\nСколько возможностей и карьерных достижений может пройти мимо тебя? Сколько'\
                ' времени ты продолжишь тратить на рутинные задачи, которые можно автоматизировать?'\
                ' \n<b>Не упусти шанс сделать следующий шаг и получить знания, которые будут работать'\
                ' на тебя. Наш флагманский курс по Excel и Google Таблицам создан для того, чтобы ты'\
                ' мог полностью раскрыть свой потенциал</b>'
        
        builder.row(types.InlineKeyboardButton(
            text='Занять место на курсе',
            url=self.urls['lk'])
        )

        self.bot.rest.send_mail(self.user_id, 17)
        await self.photo_message(self.user_id, 'assets/images/4-10.png')
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())
    
    # async def lesson_4_9(self):
    #     builder = InlineKeyboardBuilder()
    #     msg =   'Ну что ж, осталось всего 59 минут для того, чтобы воспользоваться накопленными'\
    #             ' бонусами и забронировать место на нашем курсе по лучшей цене.'\
    #             ' \n\n<b>Если тебя что-то останавливает, можешь поделиться с Ренатом, что именно - или'\
    #             ' просто оставить заявку, чтобы сохранить за собой место по лучшей цене и получить'\
    #             ' ответы на все волнующие вопросы</b>👐'
        
    #     builder.row(types.InlineKeyboardButton(
    #         text='Поговорить с Ренатом',
    #         url=self.urls['renat'])
    #     )
    #     builder.row(types.InlineKeyboardButton(
    #         text='Сохранить за собой место по лучшей цене',
    #         url=self.urls['lk'])
    #     )

    #     # await self.photo_message(self.user_id, 'assets/images/.png')
    #     await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())
    
    async def lesson_4_7(self):
        builder = InlineKeyboardBuilder()
        msg =   '<b>К сожалению, твои бонусные монеты сгорели, а вместе с ними и твоя скидка...</b>'\
                ' \n\nНадеемся, что мы увидим тебя в команде Бонни и слайд и выведем твои таблицы, а может'\
                ' быть и слайды на новый уровень!'\
                ' \nА пока будем очень благодарны твоей обратной связи по нашему мини-курсу. Мы очень'\
                ' старались сделать его полезным, а твоя обратная связь поможет увидеть наши сильные и'\
                ' слабые стороны. Заранее спасибо тебе за помощь, это бесценно❤️'
        
        builder.row(types.InlineKeyboardButton(
            text='Получить последний шанс на скидку',
            url=self.urls['lk'])
        )
        builder.row(types.InlineKeyboardButton(
            text='Поделиться обратной связью',
            url=self.urls['renat'])
        )

        await self.photo_message(self.user_id, 'assets/images/4-11.png')
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())
    
    async def lesson_4_8(self):
        builder = InlineKeyboardBuilder()
        msg =   '<b>Что делать дальше?</b>'\
                ' За 4 дня обучения на мини-курсе по сводным таблицам ты прошел по основным темам, которые являются фундаментом для работы с данными.'\
                ' Ты научился:'\
                ' \n • Строить сводные таблицы и анализировать данные'\
                ' \n • Настраивать макет таблиц и использовать фильтры'\
                ' \n • Проводить вычисления и рассчитывать доли'\
                ' \n • Использовать сводные таблицы для решения реальных задач'\
                ' \n\n<i>Многие наши ученики на этом этапе чувствуют себя более уверенно, но иногда возникает вопрос: "Как мне применить все это на практике?". И на этом моменте главное — не останавливаться. Именно сейчас настало время усилить свои навыки, чтобы использовать весь потенциал Excel и Google Таблиц и изменить свою рабочую рутину.</i>'\
                ' \n\nИ что же дальше?'\
                ' \nТеперь, когда ты поработал над базовыми навыками, представь, как ты сможешь:'\
                ' \n🤖Автоматизировать рутинные задачи с помощью макросов'\
                ' \n💡Создавать сложные аналитические модели, которые помогут тебе принимать обоснованные решения'\
                ' \n🆙Повысить свою эффективность в несколько раз и сохранить кучу времени и ресурса для решения самых интересных и важные вопросов'\
                '\n\n<b>А ещё: мы решили сохранить уникальные условия для студентов, которые прошли наш мини-курс по таблицам, и поэтому зафиксировали за тобой скидку 30%🎁'\
                'Нажимай на кнопку ниже, вводи промокод СВОДНЫЕ и оставляй заявку, чтобы успеть воспользоваться специальными условиями!</b>'\
        
        builder.row(types.InlineKeyboardButton(
            text='Хочу попасть на флагманский курс',
            url=self.urls['course'])
        )

        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())
    
    async def lesson_4_9(self):
        builder = InlineKeyboardBuilder()
        msg =   'Привет! Это Ренат Шагабутдинов, и я хотел бы лично обратиться к тебе. Я горжусь тем, что ты доверился мне и академии Bonnie&Slide и прошел наш мини-курс.'\
                ' \n\n<b>Но знаешь что? Это только начало</b>🙌'\
                ' \n\nНавык работы с таблицами актуален сейчас, был актуален давно и будет еще очень долго актуален, потому что с таблицами работают практически все. Это и профессии, которые традиционно ассоциируются с большим объемом данных: с аналитикой, с финансами; и профессии, которые могут показаться очень творческими.'\
                ' \n\nНам важно уметь разбираться с данными, обновлять их, оптимизировать, автоматизировать. И вот, что может помочь тебе справиться с этими задачами:'\
                ' \n • Глубокое погружение в продвинутые функции Excel и Google Таблиц: мы научим тебя работать с макросами, сложными формулами и инструментами визуализации данных, которые сделают тебя незаменимым специалистом'\
                ' \n • Практическое обучение: все знания, которые ты получишь, будут сразу же применяться на практике. Ты не просто изучаешь теорию — ты практикуешься урок за уроком'\
                ' \n • Персональный подход и поддержка: мы понимаем, что у каждого свои цели и задачи. Именно поэтому наши кураторы всегда на связи, чтобы помочь тебе в любой момент'\
                ' \n\nЕсли ты хочешь расти и развиваться, выходить на новый уровень в своей карьере и получать заслуженное признание за свои навыки, этот курс — именно то, что тебе нужно. Мы создавали его, опираясь на многолетний опыт и знание потребностей рынка.'\
                ' \n\n<b>Присоединяйся к нашей команде и открывай для себя новые горизонты. Ссылка на регистрацию ниже — не упусти свой шанс.</b>'\

        builder.row(types.InlineKeyboardButton(
            text='Прокачать свои навыки',
            url=self.urls['course'])
        )

        await self.photo_message(self.user_id, 'assets/images/4-14.png')
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())
    
    async def lesson_4_10(self):
        builder = InlineKeyboardBuilder()
        msg =   'Ты проделал большую работу, участвуя в нашем мини-курсе по Сводным таблицам. Мы видим твой интерес и стремление развиваться, и хотим поддержать тебя в этом!'\
                ' \n\n<b>Мы подготовили для тебя специальный бонус. Забирай по ссылке ниже все видео-уроки с нашего мини-курса</b>'\
                ' \n\nТвои навыки работы с данными могут существенно повлиять на твою карьеру и эффективность. Мы знаем, что ты уже сделал значительный шаг вперед, но настоящий успех приходит с постоянным развитием и углублением знаний.'\
                ' \n<i>Спасибо за твоё стремление к знаниям и за активное участие в нашем курсе. До встречи на основной программе!</i>🥰'\
                ' \n🎁<b>P.S.: твоя скидка 30% действительна по промокоду СВОДНЫЕ</b>'\
        
        builder.row(types.InlineKeyboardButton(
            text='Забрать видео-уроки',
            url=self.urls['lk'])
        )
        builder.row(types.InlineKeyboardButton(
            text='Хочу на флагманский курс',
            url=self.urls['course'])
        )

        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())
    
    async def lesson_4_11(self):
        builder = InlineKeyboardBuilder()
        msg =   'Мы знаем, что у тебя могут быть сомнения. Мы все сталкиваемся с моментами, когда кажется, что обучение новому может быть слишком сложным. Но давай попробуем разобраться с самыми распространёнными переживаниями, уверены, что тебе знакомы некоторые (а может и все) из них.'\
                ' \n\n⏰<b>У меня нет времени на обучение</b>'\
                ' \nДа, у каждого из нас плотный график. И, конечно, обучение не должно занимать весь твой день. Мы специально разработали наш флагманский курс так, чтобы ты мог обучаться в комфортном для тебя темпе, в любое время и с любого устройства.  Наша гибкая программа и доступ к записям уроков позволяют вам учиться, когда тебе удобно — даже если это 15-20 минут в день.'\
                ' \n\n🤔<b>Я боюсь, что это слишком сложно для меня</b>'\
                ' \nЭто нормально — почти каждый, кто приходит к нам, сталкивается с этой мыслью. Поэтому мы разбиваем сложные темы на простые шаги и поддерживаем тебя на каждом этапе. Курс начинается с основ и постепенно усложняется, давая тебе уверенность в своих силах, а команда кураторов всегда готова ответить на вопросы'\
                ' \n\n✅<b>Я уже использую Excel, мне достаточно текущего уровня</b>'\
                ' \nМногие думают, что базовые знания Excel уже позволяют работать эффективно. Но представь, что ты сможешь автоматизировать рутинные задачи, сократить не просто часы, а целые дни, которые тратятся на отчеты или другие трудоёмкие задачи, впечатлить коллег и руководство продвинутыми аналитическими инструментами'\
                ' \nНа нашем курсе ты научишься использовать такие мощные функции как макросы, сводные таблицы, сложные формулы, использовать диаграмму Ганта и строить дашборды'\
                ' \n\n<b>Ну что, теперь ты готов начать? Просто кликни на кнопку ниже и давай расти вместе!</b>'\
        
        builder.row(types.InlineKeyboardButton(
            text='Зарегистрироваться на курс',
            url=self.urls['course'])
        )

        # await self.photo_message(self.user_id, 'assets/images/4-11.png')
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())
    
    async def lesson_4_12(self):
        builder = InlineKeyboardBuilder()
        msg =   'Пиф-паф! Хотим поделиться с тобой вдохновляющей историей нашей студентки Александры Фокиной, которая, возможно, окажется для тебя знакомой и близкой.'\
                ' \n\nАлександра работает в финансах и, как и многие из нас, ежедневно сталкивается с огромным объемом данных. До прохождения нашего флагманского курса Александра пользовалась Excel была активным пользователем Excel, но она поняла, что можно и нужно работать эффективнее👆'\
                ' \n\nЗнакомо? Александра искала способ сделать свою работу проще, и вот, что произошло после курса:'\
                ' \n⏰<b>Ускорение работы с данными</b>:  научилась использовать продвинутые функции: ИНДЕКС+ПОИСКПОЗ, XLOOKUP, СУММПРОИЗВ, GETPIVOTDATA. Это позволило ей обрабатывать и сортировать данные быстрее и с меньшими усилиями'\
                ' \n❤️<b>Повышение уверенности</b>: благодаря полученным знаниям и поддержке кураторов, она стала чувствовать себя ещё увереннее в своих навыках'\
                ' \n\nНа нашем курсе по Excel Александра сделала важный шаг для своего роста, и мы были рады быть частью этого пути, и, конечно, будем рады помочь и тебе.'\
                ' \nПереходи по ссылке ниже и оставляй заявку на наш флагманский курс по специальной цене со скидкой 30% (промокод СВОДНЫЕ)  '\
                ' \n\nДо встречи!'\
        
        builder.row(types.InlineKeyboardButton(
            text='Хочу как Александра',
            url=self.urls['course'])
        )

        await self.photo_message(self.user_id, 'assets/images/4-15.png')
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())
    
    async def lesson_4_13(self):
        builder = InlineKeyboardBuilder()
        msg =   'Представь себе ситуацию (а может тебе и представлять не надо): ты тратишь целый день на подготовку отчета для руководства. Все идет по плану, пока в последний момент не обнаруживается ошибка в расчетах. Вся работа идет насмарку, и тебе приходится переделывать ВЕСЬ отчет😰'\
                ' \nИли другой случай — ты видишь, как коллеги легко справляются с задачами, используя сложные формулы и сводные таблицы, а тебе приходится вручную просматривать сотни строк данных, чтобы найти нужную информацию, и, глядя на этих коллег, ты чувствуешь зависть.'\
                ' \n\nЗнакомо?'\
                ' \n\n🔥<b>Тогда у тебя есть ещё 24 часа, чтобы попасть на наш флагманский курс по Excel и Google Таблицам по специальной цене со скидкой 30%! Не упусти эту возможность и воспользуйся промокодом СВОДНЫЕ</b>🔥'\
        
        builder.row(types.InlineKeyboardButton(
            text='Попасть на курс',
            url=self.urls['course'])
        )

        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())
    
    async def lesson_4_14(self):
        builder = InlineKeyboardBuilder()
        msg =   '<b>Сегодня — последний день, когда у тебя есть возможность присоединиться к нашему флагманскому курсу по Excel и Google Таблицам по специальной цене. Это уникальный шанс, который больше не повторится!</b>🏁'\
                ' \n\nЧто ты получаешь:'\
                ' \n • Полный доступ к нашему курсу: мы научим тебя всему, что нужно для эффективной работы с данными, от базовых функций до продвинутых инструментов анализа'\
                ' \n • Бонусные материалы: эксклюзивные PDF-гайды и дополнительные курсы, которые помогут тебе ещё быстрее освоить навыки и применить их на практике'\
                ' \n • Обратная связь и поддержка: ты не останешься наедине с трудностями — наши кураторы всегда готовы помочь и ответить на все ваши вопросы'\
                ' \n\n<i>Если ты хочешь уже до конца этого года вырасти в своих профессиональных навыках, то  чем быстрее ты начнешь, тем быстрее увидишь результаты!</i>'\
                ' \n👇Нажми здесь, чтобы зарегистрироваться прямо сейчас👇'\
        
        builder.row(types.InlineKeyboardButton(
            text='Забрать последнее место по специальной цене',
            url=self.urls['course'])
        )

        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())
    
    async def lesson_4_lead(self):
        msg =   'Мы рады, что получили твою заявку!'\
                ' \nСовсем скоро наш менеджер свяжется с тобой, ответит на все-все вопросы и поможет'\
                ' подобрать комфортный тариф!'\
                ' \n\n<b>Ты решил стать частью команды Bonnie&Slide и это очень крутое решение, о'\
                ' котором ты точно не пожалеешь</b>🚀'\
                ' \n\nДо встречи!'

        await self.photo_message(self.user_id, 'assets/images/4-12.png')
        await self.bot.bot.send_message(self.user_id, text=msg)


    ## GENERAL NOTIFICATIONS ##
    
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
            url=self.urls['renat'])
        )
        
        await self.photo_message(self.user_id, 'assets/images/inactive.png')
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())

    async def lesson_done(self):
        builder = InlineKeyboardBuilder()
        msg =   '<b>Задание выполнено! Поздравляем!</b>🎉🥳'\
                ' \n\nНапиши, пожалуйста, небольшой отзыв о просмотренном уроке и обратной связи от'\
                ' Рената, так мы поймём, что именно оказалось для тебя полезным и на чём нам дальше'\
                ' делать акцент, плюс вдохновишь других ребят своим зарядом и настроением!'
        
        builder.row(types.InlineKeyboardButton(
            text='Написать отзыв',
            url=self.urls['renat'])
        )
        
        self.bot.rest.set_user_lives(self.user_id, 3)
        await self.photo_message(self.user_id, 'assets/images/done.png')
        await self.bot.bot.send_message(self.user_id, text=msg, reply_markup=builder.as_markup())
    
