# settings.py
import os
from dotenv import load_dotenv
load_dotenv()

MONGO_CONNECTION = os.getenv("MONGO_CONNECTION")