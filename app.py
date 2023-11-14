import logging

from config.logger_loader import setup_logging

from api.main import run_fastapi

logger = logging.getLogger(__name__)


def main():
    setup_logging()
    run_fastapi()


if __name__ == '__main__':
    main()
