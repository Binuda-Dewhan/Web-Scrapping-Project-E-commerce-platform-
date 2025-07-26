# utils/wait_utils.py

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging

def wait_for_element(driver, by_locator, timeout=20):
    """
    Waits for an element to be present in the DOM.

    :param driver: Selenium WebDriver instance
    :param by_locator: Tuple(By.<METHOD>, 'locator_string')
    :param timeout: Maximum wait time in seconds
    :return: WebElement if found
    """
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(by_locator)  # ✅ FIXED
        )
    except TimeoutException:
        logging.error(f"Timeout: Element {by_locator} not found within {timeout} seconds.")
        return None