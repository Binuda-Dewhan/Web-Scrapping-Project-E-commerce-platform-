# scraper/product_scraper.py

import logging
import time
from selenium.webdriver.common.by import By
from utils.json_utils import load_product_json, update_product_json
from utils.wait_utils import wait_for_element

class ProductDetailScraper:
    def __init__(self, driver):
        self.driver = driver

    def scrape_product_page(self, json_path):
        """
        Loads a product JSON, opens the product URL, and scrapes full specs & all reviews.
        """
        data = load_product_json(json_path)
        url = data.get("product_url")

        if not url:
            logging.warning(f"No URL found in {json_path}. Skipping.")
            return

        self.driver.get(url)
        time.sleep(3)  # Allow basic load

        # ✅ 1. Scrape Full Specs (as dictionary)
        specs = self.extract_specifications()
        
        # ✅ 2. Close specs sheet if open
        try:
            close_btn = self.driver.find_element(
                By.CSS_SELECTOR,
                "button[data-testid='brix-sheet-closeButton']"
            )
            if close_btn.is_displayed() and close_btn.is_enabled():
                close_btn.click()
                logging.info("✅ Closed specification sheet.")
                time.sleep(2)
        except Exception:
            logging.info("ℹ️ No spec sheet to close, or already closed.")
        
        # ✅ 3. Scrape Reviews (all pages)
        reviews = self.extract_all_reviews()

        # ✅ 4. Update JSON file
        update_product_json(json_path, {
            "full_specs": specs,
            "all_reviews": reviews
        })

        logging.info(f"✅ Updated {json_path} with full specs & reviews.")

    def extract_specifications(self):
        try:
            from selenium.webdriver.common.by import By
            from utils.wait_utils import wait_for_element

            # ✅ First click the "Specifications" button to expand the section
            try:
                spec_button = wait_for_element(self.driver, (
                    By.XPATH, "//button[.//h3[text()='Specifications']]"
                ), timeout=10)

                if spec_button:
                    spec_button.click()
                    logging.info("Clicked 'Specifications' to reveal spec details.")
                    time.sleep(2)  # small wait for animation/rendering

            except Exception as e:
                logging.warning(f"'Specifications' button not found or not clickable: {e}")
                return "N/A"

            # ✅ Now wait for the spec blocks to load
            wait_for_element(self.driver, (By.CSS_SELECTOR, "div.dB7j8sHUbncyf79K"), timeout=10)
            spec_blocks = self.driver.find_elements(By.CSS_SELECTOR, "div.dB7j8sHUbncyf79K")

            specs = {}
            for block in spec_blocks:
                try:
                    label_elem = block.find_element(By.CSS_SELECTOR, "div.font-weight-medium")
                    value_elem = block.find_element(By.CSS_SELECTOR, "div.pl-300")

                    label = label_elem.text.strip()
                    value = value_elem.text.strip()

                    if label and value:
                        specs[label] = value
                except Exception:
                    continue  # skip malformed entries

            return specs if specs else "N/A"

        except Exception as e:
            logging.warning(f"Failed to extract specs: {e}")
            return "N/A"

    def extract_all_reviews(self):
        all_reviews = []

        try:
            # ✅ Step 1: Scroll down to bring "See All Customer Reviews" into view
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.7);")
            time.sleep(2)  # Wait for lazy load

            # ✅ Step 2: Click "See All Customer Reviews" if exists
            try:
                see_all_button = wait_for_element(
                    self.driver,
                    (By.XPATH, "//button[.//span[contains(text(),'See All Customer Reviews')]]"),
                    timeout=10
                )
                if see_all_button:
                    see_all_button.click()
                    logging.info("✅ Clicked 'See All Customer Reviews' button.")
                    time.sleep(3)
                else:
                    logging.warning("⚠️ 'See All Customer Reviews' button not found.")
                    return []

            except Exception as click_err:
                logging.warning(f"⚠️ Could not click 'See All Customer Reviews': {click_err}")
                return []

            # ✅ Step 3: Begin scraping all reviews
            while True:
                wait_for_element(self.driver, (By.CSS_SELECTOR, "li.review-item"))
                review_blocks = self.driver.find_elements(By.CSS_SELECTOR, "li.review-item")

                for block in review_blocks:
                    try:
                        title = block.find_element(By.CSS_SELECTOR, "h4.review-title").text
                        body = block.find_element(By.CSS_SELECTOR, "p.pre-white-space").text
                        rating_text = block.find_element(By.CSS_SELECTOR, "p.visually-hidden").text
                        import re
                        rating_match = re.search(r"Rated ([0-9.]+) out of 5", rating_text)
                        rating = rating_match.group(1) if rating_match else "N/A"

                        all_reviews.append({
                            "title": title,
                            "body": body,
                            "rating": rating
                        })

                    except Exception:
                        continue

                # ✅ Step 4: Handle pagination using new selector
                try:
                    next_li = self.driver.find_element(By.CSS_SELECTOR, "li.inline.page.next")
                    next_link = next_li.find_element(By.TAG_NAME, "a")

                    # Only proceed if button is not disabled
                    if next_link.get_attribute("aria-disabled") == "false":
                        self.driver.execute_script("arguments[0].click();", next_link)
                        logging.info("➡️ Clicked next review page.")
                        time.sleep(2)
                    else:
                        logging.info("❌ No more review pages (Next is disabled).")
                        break
                except Exception as e:
                    logging.warning(f"⚠️ Error finding or clicking next review page: {e}")
                    break

        except Exception as e:
            logging.warning(f"Review extraction failed: {e}")

        return all_reviews


