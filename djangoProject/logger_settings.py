LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s-%(levelname)s-----%(pathname)s--in:%(funcName)s--line-%(lineno)d:::%(message)s'
        }
    },
    'handlers': {
        'info_log': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024*5,  # 5 MB
            'backupCount': 5,
            'filename': 'logs/debug.log',
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'debug_logger': {
            'handlers': ['info_log'],
            'level': 'INFO',
            'propagate': True,
        },

    }


}
