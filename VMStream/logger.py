import logging

def  get_logger(name:str) -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)-8s %(name)s: %(message)s",
        datefmt = "%H:%M:%S",
    )
    console = logging.StreamHandler()
    console .setFormatter(formatter)
    logger.addHandler(console)
    logger.propagate = False

    return logger

