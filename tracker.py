# tracker.py

def filter_sil_fonts(font_data):
    # Enforces strict equality so multi-designer/derivatives are ignored
    return [font for font in font_data if font.get("designer") == "SIL International"]
