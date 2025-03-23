# core/tag_suggester.py

import json
import os

DEFAULT_TAG_RULES = {
    "adminisztráció": ["jira", "confluence", "outlook", "teams"],
    "fejlesztés": ["visual studio", "pycharm", "vscode", "code"],
    "szünet": ["youtube", "spotify", "netflix", "discord", "steam"],
    "verziókezelés": ["github", "gitlab"],
    "egyéb": [],
    "inaktivitás": [""]
}

CONFIG_PATH = "config/tags.json"

def load_tag_rules():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[TagSuggester] Hiba a tags.json betöltésekor: {e}")
    return DEFAULT_TAG_RULES

TAG_RULES = load_tag_rules()


def suggest_tag(window_title: str) -> str:
    title = window_title.lower().strip()

    if not title:
        return "inaktivitás"

    for tag, keywords in TAG_RULES.items():
        if any(keyword in title for keyword in keywords):
            return tag

    return "egyéb"
