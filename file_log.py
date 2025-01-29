import logging


def configurate_logger():
    logger = logging.getLogger("Process_checker")

    file_handler = logging.FileHandler("stderr.txt")
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    logger.setLevel(logging.INFO)

    return logger


logger = configurate_logger()
logger.info("Bot started successfully!")
