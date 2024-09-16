import asyncio
from notifications import Notifications
# from test_bot import TgBot
from logger import logger

class Lesson:
    def __init__(self, bot, user_id, first_name, lk_url: str, step_delays: list[int], current_lesson: int, next_lesson=None):
        # step delays contains the time in mins between each step
        # step lives contains numbers of steps where lives are lost
        self.step_delays = step_delays
        self.current_lesson = current_lesson
        # from 0 to step_delays length
        self.current_step = 0
        self.next_lesson = next_lesson
        self.bot = bot
        self.notifications = Notifications(bot, user_id, first_name, lk_url)

    async def next_step(self):
        await self.send_notification()
        self.current_step += 1
        if self.current_step < len(self.step_delays):
            self.delay = self.step_delays[self.current_step]

    async def check_homework(self, uid, delay):
        # Check every %interval% seconds
        interval = 5
        elapsed = 0
        while elapsed < delay or elapsed == 0:
            await asyncio.sleep(interval)
            elapsed += interval
            print('Time left: ' + str(delay - elapsed) + ' sec')

            lessons: list = self.bot.rest.get_user_lessons(uid)
            try:
                # lesson = lessons[-1]
                lesson = lessons[self.current_lesson - 1]
                # print(lesson)
                if (lesson['completed']):
                    # print('CHECK Completed')
                    return 'completed'
                elif (lesson['received']):
                    # print('CHECK Received')
                    return 'received'
                elif (lesson['overdue']):
                    # print('CHECK Overdue')
                    return 'overdue'
            except Exception as e:
                logger.exception(e)
                return 'unknown'
            # print('CHECK False')

        # If not received/completed after delay
        return False
    
    async def send_notification(self):
        # last step (24 hrs of inactivity)
        try:
            if self.current_step >= len(self.step_delays) - 1:
                if self.current_lesson == 4:
                    fun = "self.notifications.lesson_4_end()"
                else:
                    fun = "self.notifications.lesson_inactive()"
            else:
                fun = "self.notifications.lesson_" + str(self.current_lesson) + "_" + str(self.current_step) + "()"
            # print(fun)
            await eval(fun)
        except Exception as e:
            logger.exception(e)
    
    async def start_lesson(self, uid, current_step=0, delay=0):
        self.current_step = current_step
        self.delay = delay
        try:
            # Checking homework status until final step is reached
            while self.current_step < len(self.step_delays):
                status = await self.check_homework(uid, self.delay * 60)
                # Next step if hw not received/completed
                if not status:
                    await self.next_step()
                else:
                    # if hw completed, go to next lesson
                    if status == 'completed':
                        # print('HW COMPLETED')
                        fun = "self.notifications.lesson_done()"
                        await eval(fun)
                        if (self.current_lesson == 1):
                            await asyncio.sleep(0.05 * 60)
                            fun = "self.notifications.lesson_1_after_done()"
                            await eval(fun)

                        if (self.next_lesson):
                            await self.next_lesson.start_lesson(uid)
                        break

                    # if hw received, check its status every 5 min
                    elif status == 'received':
                        # print('HW RECEIVED')
                        await asyncio.sleep(0.3 * 60)

                    # if hw overdue, stop
                    elif status == 'overdue':
                        # print('HW OVERDUE')
                        await asyncio.sleep(0.3 * 60)
                        return
                    
                    else:
                        # print('HW UNKNOWN STATUS')
                        await self.next_step()

        except Exception as e:
            logger.exception(e)
    
# lesson_1 = Lesson([0,1,60,60,60,60, 60,60,240,120,480,240,1440])