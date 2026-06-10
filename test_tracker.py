# test_tracker.py
from tracker import filter_sil_fonts

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
