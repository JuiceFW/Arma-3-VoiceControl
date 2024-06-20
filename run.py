from pathlib import Path
import traceback
import logging
import sys

from src.main import recognition


BASE_DIR = Path(sys.argv[0]).parent
MODELS_FOLDER = BASE_DIR.joinpath("models")


logging_format = '%(asctime)s : %(name)s : %(levelname)s : %(message)s'

logger = logging.getLogger()
logging.basicConfig(
    level=logging.INFO,
    format=logging_format
)
fh = logging.FileHandler(
    "logs.log",
    encoding='utf-8'
)
fh.setFormatter(logging.Formatter(logging_format))
logger.addHandler(fh)


def main():
    try:
        recognition(MODELS_FOLDER)
    except:
        logger.critical(traceback.format_exc())


if __name__ == "__main__":
    main()
    