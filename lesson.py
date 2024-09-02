import asyncio
from notifications import Notifications
# from test_bot import TgBot

class Lesson:
    def __init__(self, bot, tg_user, lk_url: str, step_delays: list[int], step_lives: list[int], current_lesson: int, next_lesson=None):
        # step delays contains the time in mins between each step
        # step lives contains numbers of steps where lives are lost
        self.step_delays = step_delays
        self.step_lives = step_lives
        self.current_lesson = current_lesson
        # from 0 to step_delays length
        self.current_step = 0
        self.next_lesson = next_lesson
        self.bot = bot
        self.notifications = Notifications(bot, tg_user, lk_url)

    async def next_step(self):
        await self.send_notification()
        self.current_step += 1

    async def check_homework(self, uid, delay):
        # Check every %interval% seconds
        interval = 1
        elapsed = 0
        while elapsed < delay or elapsed == 0:
            await asyncio.sleep(interval)
            elapsed += interval
            
            lessons: list = self.bot.rest.get_user_lessons(uid)
            try:
                # lesson = lessons[-1]
                lesson = lessons[self.current_lesson - 1]
                print(lesson)
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
                print(e)
                return 'unknown'
            print('CHECK False')

        # If not received/completed after delay
        return False
    
    async def send_notification(self):
        # last step (24 hrs of inactivity)
        if self.current_step >= len(self.step_delays) - 1:
            fun = "self.notifications.lesson_inactive()"
        else:
            fun = "self.notifications.lesson_" + str(self.current_lesson) + "_" + str(self.current_step) + "()"
        print(fun)
        # await eval(fun)
    
    async def start_lesson(self, uid):
        # Checking homework status while final step not reached
        while self.current_step < len(self.step_delays):
            status = await self.check_homework(uid, self.step_delays[self.current_step] * 60)
            # Next step if hw not received/completed
            if not status:
                await self.next_step()
            else:
                # if hw completed, go to next lesson
                if status == 'completed':
                    print('HW COMPLETED')
                    if (self.next_lesson):
                        await self.next_lesson.start_lesson(uid)
                    break
                # if hw received, check its status every 5 min
                elif status == 'received':
                    print('HW RECEIVED')
                    await asyncio.sleep(0.3 * 60)
                # if hw overdue
                elif status == 'overdue':
                    print('HW OVERDUE')
                    await asyncio.sleep(0.3 * 60)
                    return
                else:
                    print('HW UNKNOWN STATUS')
                    await asyncio.sleep(0.5 * 60)
    
# lesson_1 = Lesson([0,1,60,60,60,60, 60,60,240,120,480,240,1440])