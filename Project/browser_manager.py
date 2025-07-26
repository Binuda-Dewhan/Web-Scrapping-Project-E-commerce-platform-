import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config import PAGE_LOAD_TIMEOUT, USER_AGENT

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

logging.basicConfig(
    filename='logs/scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class BrowserManager:
    _driver = None

    @classmethod
    def get_driver(cls):
        if cls._driver is None:
            try:
                options = Options()
                # Uncomment below line to see browser window
                options.add_argument("--headless=new")  # ✅ Faster and doesn't open the UI
                options.add_argument('--disable-gpu')
                options.add_argument('--no-sandbox')
                options.add_argument("--window-size=1920,1080")

                if USER_AGENT:
                    options.add_argument(f"user-agent={USER_AGENT}")

                # ✅ Use webdriver-manager here
                service = Service(ChromeDriverManager().install())
                cls._driver = webdriver.Chrome(service=service, options=options)
                cls._driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
                logging.info("Chrome WebDriver launched with webdriver-manager.")
            except Exception as e:
                logging.error(f"Error initializing WebDriver: {e}")
                raise
        return cls._driver

    @classmethod
    def quit_driver(cls):
        if cls._driver:
            cls._driver.quit()
            logging.info("WebDriver session closed.")
            cls._driver = None
