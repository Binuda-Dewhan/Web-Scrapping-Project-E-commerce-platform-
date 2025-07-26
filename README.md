Step 1: .env Configuration
- Create a .env file to store environment-specific configurations (e.g., timeouts, user-agent, paths).
- This allows for centralized configuration and easier tuning without editing source code.

Example .env:
PAGE_LOAD_TIMEOUT=15
USER_AGENT=Mozilla/5.0 (...)

Step 2: config.py
- Read values from the .env file using dotenv.
- Define constants like page load timeout and user agent string.

Example:
from dotenv import load_dotenv
import os

load_dotenv()

PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", 15))
USER_AGENT = os.getenv("USER_AGENT", "default-user-agent")

Step 3: category_scraper.py – Scraping Laptop Listings
- Navigates to the BestBuy Laptops category page.
- Filters are already applied via URL:
  - Price: $500–$1500
  - Brands: HP, Dell, Lenovo
  - Customer Rating: 4 stars & up
- Extracts:
  - Product Name
  - Price
  - Rating
  - Review Count
  - Short Specifications
  - Product URL
- Uses utility functions for delays, waits, and saving JSON.
- Supports lazy-loading product cards by scrolling the page.

Step 4: product_scraper.py – Advanced Scraping per Product
- Loads individual JSON files from the previous step.
- Opens each product URL to extract:
  - Full technical specifications (as a dictionary)
  - All customer reviews (supports pagination)
- Appends this data to the corresponding JSON file using update_product_json.

Step 5: main.py
- Central coordinator for scraping.
- Calls:
  - LaptopCategoryScraper to extract listings
  - ProductDetailScraper to extract full specs + reviews
- Controls flow and logging.

Step 6: data_processor.py – Data Cleaning & Analysis
Processes all collected JSON files to generate reports.

 Creates product_analysis.xlsx with the following sheets:

 Sheet 1: Product Summary
- Basic data: name, price, rating, brand, specs
- Conditional formatting on price (color-coded)
- Dropdown filtering by brand
- Excel table for clean visualization

 Sheet 2: Specifications Comparison
- Matrix of technical specs (RAM, storage, CPU, screen, battery, etc.)
- Highlights best-in-class features:
  - Max RAM (green)
  - Max Battery (green)
  - Min Weight (blue)
- Excel Table for sortable comparisons

 Sheet 3: Review Analysis
- Performs sentiment analysis using TextBlob
- Labels reviews as Positive, Neutral, or Negative
- Saves results into Excel
- Also generates:
  - Word Clouds (for All / Positive / Negative reviews)
  - Sentiment score distribution chart
  - CSV of labeled reviews for future analysis

Utility Files
These are helper modules used throughout the scraping and analysis process:
- wait_utils.py – Explicit wait handling using WebDriverWait
- delay_utils.py – Applies random delays (to prevent blocking)
- json_utils.py – Save/load/update product JSON files
- browser_manager.py – Manages Selenium Chrome browser setup

Logs
- Logging is implemented throughout for debugging and traceability.
- All logs are saved to logs/analysis.log.

📦 Folder Structure
ecommerce-analytics/
├── .env                         # Environment config
├── config.py                    # Loads values from .env
├── main.py                      # Controls scraping flow
├── analysis/
│   └── data_processor.py        # Cleans + analyzes data, generates Excel & visuals
├── data/
│   └── raw/                     # Contains raw JSON files per product
├── logs/
│   └── analysis.log             # All logs stored here
├── reports/
│   ├── product_analysis.xlsx    # Final Excel output
│   ├── all_wordcloud.png
│   ├── positive_wordcloud.png
│   ├── negative_wordcloud.png
│   └── sentiment_distribution.png
├── scraper/
│   ├── category_scraper.py      # Extracts laptops from main category
│   └── product_scraper.py       # Extracts full details + reviews per product
├── utils/
│   ├── delay_utils.py
│   ├── json_utils.py
│   ├── wait_utils.py
│   └── browser_manager.py
├── requirements.txt             # Python dependencies
└── README.txt                   # (This file)

📝 Notes
- This project is modular, so you can reuse the scraper for other product categories.
- You can expand data_processor.py to include more advanced NLP, trends, or pricing alerts.
- All Excel formatting is handled using openpyxl.
