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
    mock_data = [
        {"font_family": "Charis SIL", "designer": "SIL International", "views_7_day": 1500},
        {"font_family": "David Libre", "designer": "SIL International, Meir Sadan", "views_7_day": 1200},
        {"font_family": "Roboto", "designer": "Christian Robertson", "views_7_day": 50000}
    ]
    
    result = filter_sil_fonts(mock_data)
    
    # We expect exactly 1 font ("Charis SIL") and no derivatives like David Libre
    assert len(result) == 1
    assert result[0]["font_family"] == "Charis SIL"
    
def test_append_to_csv_writes_data_with_timestamp(tmp_path):
    test_csv = tmp_path / "metrics.csv"
    sample_data = [{"font_family": "Charis SIL", "designer": "SIL International", "views_7_day": 1500}]
    
    # Act
    append_to_csv(sample_data, filename=str(test_csv))
    
    # Assert file creation and contents
    assert os.path.exists(test_csv)
    with open(test_csv, mode='r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        first_row = next(reader)
        
        assert "Date" in headers
        assert "Charis SIL" in first_row
        assert "1500" in first_row

def test_clean_and_parse_json_strips_google_prefix():
    # 1. Arrange: Create a string that mimics exactly the json that Google outputs
    # when accessing https://fonts.google.com/metadata/stats
    raw_google_string = ")]}'\n[\n  {\n    \"family\": \"Charis SIL\"\n  }\n]"
    
    # 2. Act: Pass it to our unwritten function
    result = clean_and_parse_json(raw_google_string)
    
    # 3. Assert: Verify it's a real Python list and the prefix is gone
    assert isinstance(result, list)
    assert result[0]["family"] == "Charis SIL"

