import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN = os.getenv('ADMIN').split(' ')  # add admin IDs separated by spaces in .env file

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
INVITE_LINK = os.getenv('INVITE_LINK')
