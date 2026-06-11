# tracker.py
import csv
import os
import json
import requests
from datetime import datetime

def fetch_data(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            return response.text
        return ""
    except Exception:
        return ""

def filter_sil_fonts(font_data):
    sil_fonts = []
    for font in font_data:
        designers_list = font.get("designers", [])
        
        # Check that the list has exactly 1 item and it is 'SIL International'
        if len(designers_list) == 1 and designers_list[0] == "SIL International":
            sil_fonts.append(font)
            
    return sil_fonts

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
