import logging

# from .configuration import config


# Настройка базового логгера
def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,  # Уровень логирования
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            # logging.FileHandler(f'{config.app_name}.log'),
        ]
    )
