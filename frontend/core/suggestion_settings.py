import time


class SuggestionSettings:
    def __init__(self):
        self._enabled = True
        self._rejected_titles = {}
        self._whitelist = ["chrome", "pycharm", "excel", "jegyzettömb"]  # Testekhez vagy alapértelmezett engedélyezett címek

    def enable(self):
        self._enabled = True

    def disable(self):
        self._enabled = False

    def is_enabled(self):
        return self._enabled

    def toggle(self, value: bool):
        self._enabled = value

    def dismiss_for_now(self, title, timeout=300):
        """Ideiglenesen ne ajánljuk újra ezt a címet."""
        self._rejected_titles[title] = time.time() + timeout

    def is_suggestion_allowed(self, title: str) -> bool:
        """Megvizsgálja, hogy egy adott ablakcímre jelenleg lehet-e ajánlást megjeleníteni."""
        if not self._enabled:
            return False

        # Ellenőrizze, hogy le van-e tiltva ideiglenesen
        expiry = self._rejected_titles.get(title)
        if expiry and time.time() < expiry:
            return False

        # Whitelist alapján engedélyezve van-e
        for allowed in self._whitelist:
            if allowed.lower() in title.lower():
                return True

        return False  # Nem engedélyezett, ha nincs a listában


# 🔄 Globális példány, amit bárhol importálhatsz
suggestion_settings = SuggestionSettings()

