# core/tag_styles.py

def get_tag_style(tag: str) -> dict:
    tag = tag.lower()

    styles = {
        "fejlesztés": {"color": "#A3E635", "emoji": "🧑‍💻"},
        "adminisztráció": {"color": "#60A5FA", "emoji": "🗂️"},
        "szünet": {"color": "#9CA3AF", "emoji": "☕"},
        "verziókezelés": {"color": "#F59E0B", "emoji": "🔁"},
        "inaktivitás": {"color": "#D1D5DB", "emoji": "💤"},
        "egyéb": {"color": "#FACC15", "emoji": "❓"},
    }

    return styles.get(tag, {"color": "#E5E7EB", "emoji": "❔"})  # fallback
