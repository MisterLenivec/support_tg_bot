import logging
from logging.handlers import TimedRotatingFileHandler


def logging_config(root_path, debug_value: bool) -> None:
    if debug_value:
        logging.basicConfig(
            level=logging.DEBUG,
            format='{filename}:{lineno} #{levelname} [{asctime}] - {name} - {message}',
            style='{',
            encoding='UTF-8',
            handlers=[logging.StreamHandler()],
        )
    else:
        logging.basicConfig(
            level=logging.WARNING,
            format='{filename}:{lineno} #{levelname} [{asctime}] - {name} - {message}',
            style='{',
            encoding='UTF-8',
            handlers=[
                logging.StreamHandler(),
                TimedRotatingFileHandler(
                    root_path.joinpath("logs", "bot_logs.log"),
                    encoding='UTF-8', when='midnight', interval=1, backupCount=5)],
        )
