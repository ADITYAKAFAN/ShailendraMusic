from os import getenv

from dotenv import load_dotenv

load_dotenv()

que = {}
SESSION_NAME = getenv("SESSION_NAME", "session")
BOT_TOKEN = getenv("BOT_TOKEN")
BOT_NAME = getenv("BOT_NAME")
QUE_IMG = getenv("QUE_IMG", "https://telegra.ph/file/fa5805751e44608b1e162.png")
AUD_IMG = getenv("AUD_IMG", "https://telegra.ph/file/fa5805751e44608b1e162.png")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")

admins = {}
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")

DURATION_LIMIT = int(getenv("DURATION_LIMIT", "10"))

COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ ! \ .").split())

SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))
