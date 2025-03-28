# core/debug_logger.py

class DebugLogger:
    terminal_widget = None
    enabled = False

    @classmethod
    def initialize(cls, widget, enabled):
        cls.terminal_widget = widget
        cls.enabled = enabled

    @classmethod
    def log(cls, message):
        if cls.enabled and cls.terminal_widget:
            cls.terminal_widget.appendPlainText(message)
