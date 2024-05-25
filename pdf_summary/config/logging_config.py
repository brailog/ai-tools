import logging
from logging.config import dictConfig

# Configuração básica de logging
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "DEBUG",  # Console exibirá mensagens de DEBUG e acima
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": "app.log",
            "level": "INFO",  # Arquivo registrará mensagens de INFO e acima
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": "DEBUG",  # Logger raiz configurado para DEBUG e acima
        },
    },
}

dictConfig(logging_config)
logger = logging.getLogger(__name__)
