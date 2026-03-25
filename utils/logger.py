import logging
import os

os.makedirs("reports/logs", exist_ok=True)

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s")

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(fmt)

        fh = logging.FileHandler("reports/logs/test_run.log")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(fmt)

        logger.addHandler(ch)
        logger.addHandler(fh)
    return logger
