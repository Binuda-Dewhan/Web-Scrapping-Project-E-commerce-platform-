# scraper/category_scraper.py

import logging
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from utils.wait_utils import wait_for_element
from utils.delay_utils import apply_random_delay
from utils.json_utils import save_product_json  # ← Import this

class LaptopCategoryScraper:
    """
    Scrapes filtered laptop product listings from BestBuy.
    Filters (already applied in URL):
    - Price: $500–$1500
    - Brands: HP, Dell, Lenovo
    - Rating: 4+ stars
    """

    def __init__(self, driver):
        self.driver = driver
        self.products = []

    def navigate_to_laptops(self):
        """
        Navigates to the filtered laptops category page after handling country selection.
        """
        try:
            base_url = "https://www.bestbuy.com/"
            logging.info("Opening BestBuy homepage...")
            self.driver.get(base_url)
            apply_random_delay()

            # ✅ Step 1: Click "United States" if splash appears
            try:
                from selenium.webdriver.common.by import By
                from utils.wait_utils import wait_for_element

                us_link = wait_for_element(self.driver, (By.CSS_SELECTOR, "a.us-link"), timeout=5)
                if us_link:
                    us_link.click()
                    logging.info("Selected 'United States' on splash screen.")
                    apply_random_delay()
                else:
                    logging.info("No splash screen found. Proceeding directly.")

            except Exception as splash_err:
                logging.warning(f"Splash handling skipped or failed: {splash_err}")

            # ✅ Step 2: Navigate to the filtered laptops URL with "intl=nosplash"
            laptops_url = (
                "https://www.bestbuy.com/site/searchpage.jsp?"
                "id=pcat17071&qp=currentprice_facet%3DPrice%7E500+to+1500"
                "%5Ebrand_facet%3DBrand%7ELenovo%5Ebrand_facet%3DBrand%7EHP"
                "%5Ebrand_facet%3DBrand%7EDell%5Ecustomerreviews_facet%3D"
                "Customer+Rating%7E4+%26+Up&st=laptops&intl=nosplash"
            )

            self.driver.get(laptops_url)
            apply_random_delay()
            logging.info("Navigated to filtered laptops category.")

        except Exception as e:
            logging.error(f"Error in laptop navigation: {e}")
            raise
        
    def scroll_to_load_all_products(self, pause_time=2, max_attempts=20):
        """
        Scrolls slowly down the page to load all lazy-loaded product cards.
        Stops when no new content is loaded after several attempts.
        """
        import time

        last_height = self.driver.execute_script("return document.body.scrollHeight")
        attempts = 0

        while attempts < max_attempts:
            self.driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(pause_time)
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                attempts += 1
            else:
                attempts = 0  # reset if new content is loaded

            last_height = new_height
            
    # def extract_all_pages(self):
    #     """
    #     Handles pagination: scrapes product cards across all pages.
    #     """
    #     try:
    #         page = 1
    #         while True:
    #             logging.info(f"📄 Scraping Page {page}")
    #             self.extract_product_cards()
    #             apply_random_delay()

    #             try:
    #                 # ✅ Find "Next" button using correct selector
    #                 next_button = self.driver.find_element(By.CSS_SELECTOR, "a.pagination-arrow[aria-label='Next page']")
                    
    #                 # Check if it's disabled
    #                 if next_button.get_attribute("aria-disabled") == "true":
    #                     logging.info("❌ 'Next' button is disabled. Reached last page.")
    #                     break

    #                 # ✅ Click "Next"
    #                 self.driver.execute_script("arguments[0].click();", next_button)
    #                 logging.info("➡️ Clicked next page.")
    #                 page += 1
    #                 apply_random_delay()

    #             except Exception as e:
    #                 logging.info("✅ Reached last page or 'Next' button not found.")
    #                 break

    #     except Exception as e:
    #         logging.error(f"❌ Error during pagination scraping: {e}")



            
    def extract_product_cards(self):
        """
        Extracts product information after ensuring product cards are visible.
        """
        try:
            apply_random_delay()
            
            # Scroll down gradually to load all product cards
            self.scroll_to_load_all_products()

            # ✅ Wait until at least one product card is visible
            wait_for_element(self.driver, (By.CSS_SELECTOR, "ul.plp-product-list > li"), timeout=15)
            product_cards = self.driver.find_elements(By.CSS_SELECTOR, "ul.plp-product-list > li")

            logging.info(f"Found {len(product_cards)} product cards.")

            for idx, card in enumerate(product_cards):
                logging.info(f"Scraping product card {idx + 1}...")

                try:
                    # ✅ Product Name from brand (first-title) and model (value)
                    brand_elem = card.find_elements(By.CSS_SELECTOR, "span.first-title")
                    model_elem = card.find_elements(By.CSS_SELECTOR, "span.value")

                    brand = brand_elem[0].text.strip() if brand_elem else ""
                    model = model_elem[0].text.strip() if model_elem else ""

                    # Combine them into full name
                    if brand or model:
                        name = f"{brand} {model}".strip()
                    else:
                        name = "N/A"


                    # ✅ Price (medium-customer-price class)
                    price_elem = card.find_elements(By.XPATH, ".//div[@data-testid='medium-customer-price']")
                    price = price_elem[0].text.replace("$", "").replace(",", "").strip() if price_elem else "N/A"

                    # ✅ Rating (from visually-hidden tag)
                    rating_elem = card.find_elements(By.CSS_SELECTOR, "p.visually-hidden")
                    rating = "N/A"

                    if rating_elem:
                        rating_text = rating_elem[0].text.strip()  # e.g., "Rating 4.6 out of 5 stars with 68 reviews"
                        try:
                            import re
                            match = re.search(r"Rating\s+([0-9.]+)\s+out of 5", rating_text)
                            if match:
                                rating = match.group(1)
                        except Exception as e:
                            logging.warning(f"Error parsing rating from visually-hidden: {e}")


                    # ✅ Reviews count (from c-reviews order-2)
                    reviews_elem = card.find_elements(By.XPATH, ".//span[contains(@class, 'c-reviews') and contains(@class, 'order-2')]")
                    review_count = reviews_elem[0].text.strip("()") if reviews_elem else "0"

                    # ✅ Specifications from product-title h2 and URL from <a>
                    link_elem = card.find_elements(By.CSS_SELECTOR, "a.product-list-item-link")
                    product_url = link_elem[0].get_attribute("href") if link_elem else None

                    spec_elem = card.find_elements(By.CSS_SELECTOR, "h2.product-title")
                    if spec_elem:
                        specs = spec_elem[0].get_attribute("title") or spec_elem[0].text.strip()
                    else:
                        specs = "N/A"

                    # ✅ Save product data
                    self.products.append({
                        "name": name,
                        "price": price,
                        "rating": rating,
                        "reviews": review_count,
                        "specs": specs,
                        "product_url": product_url
                    })

                    # logging.info(f"✅ Scraped: {name} | ${price} | Rating: {rating} | Reviews: {review_count}")
                    
                    # Inside your loop after you build the product_data dictionary
                    save_product_json({
                        "name": name,
                        "price": price,
                        "rating": rating,
                        "reviews": review_count,
                        "specs": specs,
                        "product_url": product_url
                    })

                except Exception as e:
                    logging.warning(f"⚠️ Error parsing product card {idx + 1}: {e}")

            logging.info(f"✅ Finished scraping. Total products extracted: {len(self.products)}")

        except Exception as e:
            logging.error(f"❌ Error extracting product cards: {e}")
            


    def get_spec_snippet(self, card):
        """
        Retrieves short spec or model info (if available).
        """
        try:
            return card.find_element(By.CSS_SELECTOR, "div.sku-model").text
        except Exception:
            return "N/A"

    def get_products(self):
        return self.products
