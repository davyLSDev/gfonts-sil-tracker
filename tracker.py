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
        
def clean_and_parse_json(raw_text):
    # Strips the leading security characters, newlines, and spaces
    cleaned_text = raw_text.lstrip(")]}'\n ")
    return json.loads(cleaned_text)

def filter_sil_fonts(font_data):
    sil_fonts = []
    for font in font_data:
        designers_list = font.get("designers", [])
        
        # Check that the list has exactly 1 item and it is 'SIL International'
        if len(designers_list) == 1 and designers_list[0] == "SIL International":
            sil_fonts.append(font)
            
    return sil_fonts

def append_to_csv(data, filename="font_metrics.csv"):
    headers = ["Date", "Font", "Weekly Views", "Lifetime Views"]
    today = datetime.now().strftime("%Y-%m-%d")
    
    existing_rows = []
    if os.path.isfile(filename):
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_rows.append(row)
                
    fresh_rows = []
    for font in data:
        date_range = font.get("viewsByDateRange", {}) or {}
        day_7_stats = date_range.get("7day", {}) or {}
        weekly_views = day_7_stats.get("views", 0)
        lifetime_views = font.get("totalViews", 0)
        
        fresh_rows.append({
            "Date": today,
            "Font": font.get("family"),
            "Weekly Views": weekly_views,
            "Lifetime Views": lifetime_views
        })
        
    all_rows = fresh_rows + existing_rows
    
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(all_rows)

if __name__ == "__main__":
    TARGET_URL = "https://fonts.google.com/metadata/stats"
    
    print("Fetching live analytics metrics from Google Fonts...")
    raw_payload = fetch_data(TARGET_URL)
    
    if raw_payload:
        parsed_list = clean_and_parse_json(raw_payload)
        sil_only_fonts = filter_sil_fonts(parsed_list)
        
        if sil_only_fonts:
            append_to_csv(sil_only_fonts)
            print(f"\nSuccess! Tracked {len(sil_only_fonts)} sole-designer SIL fonts.")
            for font in sil_only_fonts:
                print(f" -> {font['family']}: {font['totalViews']:,} overall views.")
        else:
            print("No fonts found matching SIL International as the sole author.")
    else:
        print("Failed to pull raw endpoint metrics from the network.")

