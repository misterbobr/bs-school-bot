from os import getenv
from dotenv import load_dotenv
import test_bot

load_dotenv(override=True)
TG_API_KEY = getenv('TG_API_KEY')
SITE_URL = getenv('SITE_URL')
REST_API_URL = getenv('REST_API_URL')
REST_API_KEY = getenv('REST_API_KEY')
UPLOADS_PATH = getenv('UPLOADS_PATH')
bot = test_bot.TgBot(TG_API_KEY, SITE_URL, REST_API_URL, REST_API_KEY, UPLOADS_PATH)