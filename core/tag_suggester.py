# core/tag_suggester.py

def suggest_tag(window_title: str) -> str:
    title = window_title.lower()

    if any(keyword in title for keyword in ["jira", "confluence", "outlook", "teams"]):
        return "adminisztráció"
    elif any(keyword in title for keyword in ["visual studio", "pycharm", "vscode", "code", "projekt", "dev"]):
        return "fejlesztés"
    elif any(keyword in title for keyword in ["github", "gitlab"]):
        return "verziókezelés"
    elif any(keyword in title for keyword in ["youtube", "spotify", "netflix", "discord", "steam"]):
        return "szünet"
    elif any(keyword in title for keyword in ["excel", "word", "powerpoint", "munka", "work", "document"]):
        return "munka"
    elif title.strip() == "":
        return "inaktivitás"
    else:
        return "egyéb"
