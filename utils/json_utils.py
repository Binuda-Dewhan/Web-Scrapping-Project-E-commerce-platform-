# utils/json_utils.py

import os
import json
import logging

def save_product_json(product_data, output_dir="data/raw"):
    try:
        # Clean filename using product name or unique ID
        safe_name = product_data.get("name", "product").replace("/", "-").replace("\\", "-").replace(" ", "_")
        filename = f"{safe_name[:50]}.json"  # Limit to 50 chars to avoid issues
        filepath = os.path.join(output_dir, filename)

        # Create dir if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Save JSON
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(product_data, f, ensure_ascii=False, indent=4)

        logging.info(f"📝 Saved product JSON: {filepath}")
    except Exception as e:
        logging.error(f"❌ Error saving product JSON: {e}")
        
def load_product_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def update_product_json(filepath, new_data: dict):
    data = load_product_json(filepath)
    data.update(new_data)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
