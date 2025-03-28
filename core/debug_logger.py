import sys

class DebugLogger:
    terminal_widget = None
    enabled = False

    class OutputRedirector:
        def __init__(self, original_stream, prefix=''):
            self.original_stream = original_stream
            self.prefix = prefix

        def write(self, text):
            if text.strip() and DebugLogger.enabled and DebugLogger.terminal_widget:
                DebugLogger.terminal_widget.appendPlainText(f"{self.prefix}{text.strip()}")
            self.original_stream.write(text)

        def flush(self):
            self.original_stream.flush()

    @classmethod
    def initialize(cls, widget, enabled):
        cls.terminal_widget = widget
        cls.enabled = enabled
        if enabled:
            sys.stdout = cls.OutputRedirector(sys.stdout)
            sys.stderr = cls.OutputRedirector(sys.stderr, "[HIBA] ")

    @classmethod
    def log(cls, message):
        if cls.enabled and cls.terminal_widget:
            cls.terminal_widget.appendPlainText(message)
