import logging
import sys

def setup_logger(debug_mode=False):
    log_level = logging.DEBUG if debug_mode else logging.INFO

    logger = logging.getLogger()
    logger.setLevel(log_level)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s"
    )

    # Console handler (terminálba írás)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (fájlba írás)
    file_handler = logging.FileHandler("backend.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
