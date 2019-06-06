# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import requests

loggers = {
    'acceptance': logging.getLogger('acceptance'),
    'linphone': logging.getLogger('linphone'),
}


def setup_logging(config):
    file_handler = logging.FileHandler(config['default']['log_file'])

    for name, logger in loggers.items():
        logger.setLevel(logging.INFO)
        for handler in logger.handlers:
            logger.removeHandler(handler)
        logger.addHandler(file_handler)
        if config['default']['debug'].get(name):
            logger.setLevel(logging.DEBUG)

    requests.packages.urllib3.disable_warnings()


def logcall(func):
    def decorated(*args, **kwargs):
        loggers['acceptance'].debug("calling %s(%s, %s)", func.__name__, args, kwargs)
        func(*args, **kwargs)
    return decorated
