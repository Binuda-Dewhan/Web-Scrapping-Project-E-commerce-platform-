# 🛍️ E-Commerce Analytics Automation Project

## 📊 Overview

This project automates the scraping and analysis of laptop product data and customer reviews from a major e-commerce platform (e.g., BestBuy.com). It includes:
- Data scraping with Selenium
- Sentiment analysis with TextBlob
- Excel report generation with openpyxl
- Modular utility scripts
- Structured logs and reusable pipelines

---

## 🚀 Features

- ✅ Filter laptops by price ($500–$1500), brand (HP, Dell, Lenovo), and rating (4★+)
- ✅ Collect and store product listings and full product details in JSON
- ✅ Extract customer reviews across paginated pages
- ✅ Perform sentiment analysis on reviews (Positive, Neutral, Negative)
- ✅ Generate Excel reports with:
  - Conditional formatting
  - Pivot tables and filters
  - Comparison matrix of specs
  - Word clouds and sentiment visualizations
- ✅ Logging and modular architecture
- ✅ Configuration using `.env` and `config.py`

---

## 📦 Folder Structure

```
ecommerce-analytics/
├── .env                      # Environment config
├── config.py                 # Loads values from .env
├── main.py                   # Controls scraping flow
├── analysis/
│   └── data_processor.py     # Cleans + analyzes data, generates Excel & visuals
├── data/
│   └── raw/                  # Contains raw JSON files per product
├── logs/
│   └── analysis.log          # All logs stored here
├── reports/
│   ├── product_analysis.xlsx # Final Excel output
│   ├── all_wordcloud.png
│   ├── positive_wordcloud.png
│   ├── negative_wordcloud.png
│   └── sentiment_distribution.png
├── scraper/
│   ├── category_scraper.py   # Extracts laptops from main category
│   └── product_scraper.py    # Extracts full details + reviews per product
├── utils/
│   ├── delay_utils.py
│   ├── json_utils.py
│   ├── wait_utils.py
│   └── browser_manager.py
├── requirements.txt          # Python dependencies
└── README.md                 # (This file)
```

---

## 🛠️ Step-by-Step Breakdown

### ✅ Step 1: `.env` Configuration
- Centralized configuration using `.env` for timeout, user-agent, etc.

**Example `.env`:**
```ini
PAGE_LOAD_TIMEOUT=15
USER_AGENT=Mozilla/5.0 (...)
```

## ✅ Step 2: `config.py`

Reads values from `.env` using `python-dotenv`.

```python
from dotenv import load_dotenv
import os

load_dotenv()

PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", 15))
USER_AGENT = os.getenv("USER_AGENT", "default-user-agent")
```

---

## ✅ Step 3: `category_scraper.py`

Scrapes laptops with applied filters via URL.

- Extracts product name, price, rating, review count, short specs, and product URL  
- Uses scrolling and utility delays

---

## ✅ Step 4: `product_scraper.py`

Reads scraped product URLs and visits each product page to collect:

- Full technical specs  
- Paginated customer reviews  
- Updates JSON with detailed info

---

## ✅ Step 5: `main.py`

Acts as the orchestrator:

- Calls both scrapers  
- Manages logging and flow

## ✅ Step 6: `data_processor.py`

Processes raw JSON files to generate an Excel workbook:

### 📘 Sheet 1: Product Summary
- Basic product info  
- Conditional formatting on price  
- Dropdown filters by brand  
- Excel table layout

### 📘 Sheet 2: Specification Comparison
- Matrix format for specs  
- Highlights:
  - Max RAM, battery → 🟩 Green  
  - Min weight → 🟦 Blue

### 📘 Sheet 3: Review Analysis
- Sentiment analysis (using `TextBlob`)  
- Sentiment-labeled reviews  
- Generates:
  - Word clouds (All / Positive / Negative)  
  - Sentiment distribution chart  
  - CSV of labeled reviews

---

## 🔧 Utility Modules

| File               | Purpose                           |
|--------------------|-----------------------------------|
| `wait_utils.py`    | Explicit wait handling            |
| `delay_utils.py`   | Adds random delay between actions |
| `json_utils.py`    | Save/load/update JSON             |
| `browser_manager.py` | Chrome browser setup            |

---

## 🪵 Logging

- All operations are logged to `logs/analysis.log`  
- Helpful for debugging and status monitoring

---

## 🧪 Testing

Basic unit tests are included in the `tests/` directory.

To run them:

```bash
pytest tests/
```

---

## 📋 Requirements

Install all dependencies:

```bash
pip install -r requirements.txt
```

**Main packages used:**
- `selenium`  
- `pandas`  
- `openpyxl`  
- `nltk`  
- `matplotlib`, `seaborn`  
- `python-dotenv`

---

## 📌 Notes

- The scraper and analyzer are modular – easily extendable to other categories.  
- You can plug in more advanced NLP or price alerting if needed.

---

## 🙋 Author

**Binuda Dewhan Bandara**  
Feel free to connect or raise issues in this repo!

---

## 📜 License

This project is for academic and demo purposes only.

---

### ✅ To update your current `README.md` file:

1. Open the file in any code editor (VS Code, Notepad++, etc.)
2. Replace all existing content with the markdown above
3. Save the file
4. Commit and push:

```bash
git add README.md
git commit -m "Update README with full project description"
git push
```


