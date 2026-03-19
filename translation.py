import json

with open("translations.json", "r", encoding="utf-8") as f:
    translations = json.load(f)

LANGUAGE = "en"

widgets = []

def set_language(language):
    global LANGUAGE
    LANGUAGE = language

def translate(key):
    return translations.get(LANGUAGE, {}).get(key, f"[{key}]")

def register_widget(widget, key):
    widgets.append((widget, key))

def refresh_ui():
    for widget, key in widgets:
        widget.config(text=translate(key))