# Copyright 2015-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

import requests

loggers = {
    'acceptance': logging.getLogger('acceptance'),
    'linphone': logging.getLogger('linphone'),
    'stevedore': logging.getLogger('stevedore'),
    'wazo_test_helpers': logging.getLogger('wazo_test_helpers'),
}


def setup_logging(log_file, debug_config):
    file_handler = logging.FileHandler(log_file)

    for name, logger in loggers.items():
        logger.setLevel(logging.INFO)
        for handler in logger.handlers:
            logger.removeHandler(handler)
        logger.addHandler(file_handler)
        if debug_config.get(name):
            logger.setLevel(logging.DEBUG)

    requests.packages.urllib3.disable_warnings()


def logcall(func):
    def decorated(*args, **kwargs):
        loggers['acceptance'].debug("calling %s(%s, %s)", func.__name__, args, kwargs)
        func(*args, **kwargs)
    return decorated
