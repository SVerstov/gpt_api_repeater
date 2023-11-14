import logging

from config import load_config, setup_logging

logger = logging.getLogger(__name__)



def main():
    setup_logging()
    config = load_config()
    print(
        config.main.gpt_token
    )


if __name__ == '__main__':
    main()
