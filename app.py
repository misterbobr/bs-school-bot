from os import getenv
from dotenv import load_dotenv
import test_bot

load_dotenv(override=True)
API_KEY = getenv('TG_API_KEY')
API_URL = getenv('REST_API_URL')
bot = test_bot.TgBot(API_KEY, API_URL)