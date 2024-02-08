from pathlib import Path
from app.config import Config
import logging
from logging import config as logging_config

LOG_DIR = Path(__file__).resolve().parent.parent.joinpath('logs')

app_logging_config = {
    'version': 1,
    'loggers': {
        Config.APP_NAME: {
            'level': 'DEBUG',  # min level, filtering is done in handlers, default is WARNING if 'NOTSET'
            'handlers': ['console',
                         'info_file_handler',
                         'error_file_handler',
                         ],
        },
        'uvicorn': {  # uvicorn default access logger
            'level': 'DEBUG',
            'handlers': [
                'console',
                'info_file_handler',
            ],
        },

        'uvicorn.error': {  # uvicorn default error logger
            'level': 'WARNING',
            'handlers': [
                'console',
                'error_file_handler',
            ],
        },

        'gunicorn.access': {  # gunicorn default access logger
            'level': 'DEBUG',
            'handlers': [
                'console',
                'info_file_handler',
            ],
        },
        'gunicorn.error': {  # gunicorn default error logger
            'level': 'DEBUG',
            'handlers': [
                'console',
                'error_file_handler',
            ],
        },
    },
    'handlers': {
        'console': {
            'level': Config.LOG_LEVEL,
            'formatter': 'info',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'info_file_handler': {
            'level': Config.LOG_LEVEL,
            'formatter': 'info',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(Path(LOG_DIR).joinpath(Config.LOG_FILE_INFO)),
            'mode': 'a',
            'maxBytes': 5048576,
            'backupCount': 100
        },
        'error_file_handler': {
            'level': 'WARNING',
            'formatter': 'error',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(Path(LOG_DIR).joinpath(Config.LOG_FILE_ERROR)),
            'mode': 'a',
            'maxBytes': 5048576,
            'backupCount': 100
        }
    },
    'formatters': {
        'info': {
            'format': '%(asctime)s-%(levelname)s-%(name)s-%(module)s-%(lineno)s:: %(message)s'
        },
        'error': {
            'format': '%(asctime)s-%(levelname)s-%(name)s-%(module)s-%(lineno)s:: %(message)s'
        },
        'discord': {
            'format': '%(levelname)s-%(module)s-%(lineno)s:: %(message)s'
        }
    },
}

logging_config.dictConfig(app_logging_config)
logger = logging.getLogger(Config.APP_NAME)
logger.info(f"[START]: Logger ready for {Config.APP_NAME}")
