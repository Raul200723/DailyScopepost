from dotenv import load_dotenv
import os

load_dotenv()

APP_NAME = os.getenv("APP_NAME")
BASE_URL = os.getenv("BASE_URL")

LANGUAGE = os.getenv("LANGUAGE")
COUNTRY = os.getenv("COUNTRY")

GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")