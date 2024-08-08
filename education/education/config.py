import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")

DATA_BASE = os.environ.get("DATA_BASE")
DB_NAME = os.environ.get("DB_NAME")
USER_NAME = os.environ.get("USER_NAME")
USER_PASSWORD = os.environ.get("USER_PASSWORD")
HOST = os.environ.get("HOST")
