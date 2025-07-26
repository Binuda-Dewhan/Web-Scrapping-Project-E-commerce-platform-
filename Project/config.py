# config.py

import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://www.bestbuy.com/")
USER_AGENT = os.getenv("USER_AGENT")
WAIT_MIN = float(os.getenv("WAIT_MIN", 2))
WAIT_MAX = float(os.getenv("WAIT_MAX", 5))
PAGE_LOAD_TIMEOUT = 30
IMPLICIT_WAIT = 10
