# utils/delay_utils.py

import time
import random
import logging
from config import WAIT_MIN, WAIT_MAX

def apply_random_delay():
    """
    Applies a random delay between requests to mimic human behavior.
    """
    delay = random.uniform(WAIT_MIN, WAIT_MAX)
    logging.info(f"Applying random delay: {delay:.2f} seconds")
    time.sleep(delay)
