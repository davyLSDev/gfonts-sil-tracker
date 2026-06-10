# test_tracker.py
import os
import csv
from tracker import filter_sil_fonts
from tracker import append_to_csv

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
