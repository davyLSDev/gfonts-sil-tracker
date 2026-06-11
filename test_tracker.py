# test_tracker.py
import os
import csv
from unittest.mock import patch
from tracker import (
    fetch_data,
    filter_sil_fonts,
    append_to_csv,
    clean_and_parse_json
)

# Test A: What should happen when the internet works perfectly?
@patch('tracker.requests.get')
def test_fetch_data_returns_raw_text_on_200_success(mock_get):
    # 1. Arrange: Tell our fake 'requests.get' to simulate a successful 200 OK website response
    fake_response = mock_get.return_value
    fake_response.status_code = 200
    fake_response.text = ")]}'\n[{\"family\": \"Charis SIL\"}]"
    
    # 2. Act: Call the function we are about to build
    result = fetch_data("https://fonts.google.com/metadata/stats")
    
    # 3. Assert: Verify our function successfully extracted and returned that raw text string
    assert result == ")]}'\n[{\"family\": \"Charis SIL\"}]"

# Test B: What should happen if Google's server crashes (500 Error) or the URL is wrong (404)?
@patch('tracker.requests.get')
def test_fetch_data_returns_empty_string_on_network_failure(mock_get):
    # 1. Arrange: Tell our fake 'requests.get' to simulate a broken server response
    fake_response = mock_get.return_value
    fake_response.status_code = 500
    
    # 2. Act
    result = fetch_data("https://fonts.google.com/metadata/stats")
    
    # 3. Assert: It shouldn't crash our script; it should just return an empty string safely
    assert result == ""

def test_filter_sil_as_sole_author_fonts():
    # Arrange: Setup mock data mirroring Google's exact production format
    real_google_format_mock = [
        {
            "family": "Charis SIL",
            "designers": ["SIL International"],
            "viewsByDateRange": {"7day": {"views": 1500, "change": 0.02}}
        },
        {
            "family": "David Libre",
            "designers": ["SIL International", "Meir Sadan"],  # Not sole author! Exclude.
            "viewsByDateRange": {"7day": {"views": 1200, "change": -0.01}}
        },
        {
            "family": "Roboto",
            "designers": ["Christian Robertson"],  # Wrong author. Exclude.
            "viewsByDateRange": {"7day": {"views": 50000, "change": 0.05}}
        }
    ]
    
    # Act: Call your filtering function
    result = filter_sil_fonts(real_google_format_mock)
    
    # Assert: We expect exactly 1 font back, and it must be Charis SIL
    assert len(result) == 1
    assert result[0]["family"] == "Charis SIL"
    
def test_append_to_csv_keeps_newest_data_at_the_top(tmp_path):
    test_csv = tmp_path / "font_metrics.csv"
    headers = ["Date", "Font", "Weekly Views", "Lifetime Views"]
    
    with open(test_csv, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerow({
            "Date": "2026-06-04", 
            "Font": "Charis SIL", 
            "Weekly Views": "1000",
            "Lifetime Views": "4000000"
        })

    fresh_scraped_data = [{
        "family": "Charis SIL",
        "designers": ["SIL International"],
        "totalViews": 4119000,
        "viewsByDateRange": {"7day": {"views": 1500}}
    }]
    
    append_to_csv(fresh_scraped_data, filename=str(test_csv))
    
    with open(test_csv, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        file_headers = next(reader)
        row_1 = next(reader)
        row_2 = next(reader)
        
        assert file_headers == ["Date", "Font", "Weekly Views", "Lifetime Views"]
        assert row_1[0] == "2026-06-11"
        assert row_1[2] == "1500"
        assert row_1[3] == "4119000"
        assert row_2[0] == "2026-06-04"

def test_clean_and_parse_json_strips_google_prefix():
    # 1. Arrange: Create a string that mimics exactly the json that Google outputs
    # when accessing https://fonts.google.com/metadata/stats
    raw_google_string = ")]}'\n[\n  {\n    \"family\": \"Charis SIL\"\n  }\n]"
    
    # 2. Act: Pass it to our unwritten function
    result = clean_and_parse_json(raw_google_string)
    
    # 3. Assert: Verify it's a real Python list and the prefix is gone
    assert isinstance(result, list)
    assert result[0]["family"] == "Charis SIL"

