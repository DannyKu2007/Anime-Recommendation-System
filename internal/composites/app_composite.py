from internal.adapters.db.sqlite import create_table

import string

import logging


def prepare_application():
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s- %(filename)s:%(lineno)d - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    logger.info('starting app')

    create_table(logger)

    removing_symbols = ''.join([chr(x) for x in range(256) if chr(x) not in string.digits + string.ascii_letters + ' :!'])

    return logger, removing_symbols
