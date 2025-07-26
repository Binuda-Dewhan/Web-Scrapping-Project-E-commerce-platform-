import logging
import os
from browser_manager import BrowserManager
from scraper.category_scraper import LaptopCategoryScraper
from scraper.product_scraper import ProductDetailScraper

def main():
    driver = None
    try:
        driver = BrowserManager.get_driver()

        # ✅ STEP 1: Scrape product listings
        logging.info("🚀 Starting product card scraping...")
        category_scraper = LaptopCategoryScraper(driver)
        category_scraper.navigate_to_laptops()
        category_scraper.extract_product_cards()

        products = category_scraper.get_products()
        logging.info(f"✅ {len(products)} products saved to JSON files.")

        # ✅ STEP 2: Scrape product detail pages (specs + reviews)
        logging.info("🔍 Starting product detail scraping...")
        detail_scraper = ProductDetailScraper(driver)
        json_dir = "./data/raw/"
        for filename in os.listdir(json_dir):
            if filename.endswith(".json"):
                path = os.path.join(json_dir, filename)
                detail_scraper.scrape_product_page(path)

    except Exception as e:
        logging.error(f"❌ Exception in main(): {e}")

    finally:
        if driver:
            BrowserManager.quit_driver()

if __name__ == "__main__":
    main()
