# tracker.py
import csv
import os
import json
from datetime import datetime

def filter_sil_fonts(font_data):
    # Enforces strict equality so multi-designer/derivatives are ignored
    return [font for font in font_data if font.get("designer") == "SIL International"]

def append_to_csv(data, filename="font_metrics.csv"):
    file_exists = os.path.isfile(filename)
    headers = ["Date", "Font Family", "Designer", "7 Day Views"]
    today = datetime.now().strftime("%Y-%m-%d")
    
    with open(filename, mode='a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        if not file_exists:
            writer.writeheader()
            
        for font in data:
            writer.writerow({
                "Date": today,
                "Font Family": font.get("font_family"),
                "Designer": font.get("designer"),
                "7 Day Views": font.get("views_7_day")
            })

def clean_and_parse_json(raw_text):
    # Strips the leading security characters, newlines, and spaces
    cleaned_text = raw_text.lstrip(")]}'\n ")
    return json.loads(cleaned_text)
