# backend/tests/test_suggestion_blocking.py

from unittest.mock import patch
from frontend.core.suggestion_settings import suggestion_settings
from frontend.components.window_title_watcher import WindowTitleWatcher
from frontend.services.api_client import APIClient
from frontend.core.task_timer_manager import TaskTimerManager  # ⬅️ EZ a helyes import

def test_no_suggestion_when_task_running():
    suggestion_settings.enable()
    task_timer = TaskTimerManager()
    task_timer.start_task(999)

    watcher = WindowTitleWatcher(api_client=APIClient(), task_timer=task_timer)

    with patch("win32gui.GetForegroundWindow", return_value=1), \
         patch("win32gui.GetWindowText", return_value="Visual Studio"), \
         patch("frontend.components.window_title_watcher.SuggestTaskPopup") as mock_popup:

        watcher.check_window()
        mock_popup.assert_not_called()
