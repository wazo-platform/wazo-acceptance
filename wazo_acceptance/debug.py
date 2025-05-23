# Copyright 2015-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

import requests

loggers = {
    'linphone': logging.getLogger('linphone'),
    'stevedore': logging.getLogger('stevedore'),
    'wazo_acceptance': logging.getLogger('wazo_acceptance'),
    'wazo_test_helpers': logging.getLogger('wazo_test_helpers'),
}


def setup_logging(log_file, debug_config):
    file_handler = logging.FileHandler(log_file)

    for name, logger in loggers.items():
        logger.setLevel(logging.DEBUG if debug_config.get(name) else logging.INFO)
        for handler in logger.handlers:
            logger.removeHandler(handler)
        logger.addHandler(file_handler)

    requests.packages.urllib3.disable_warnings()


def logcall(func):
    def decorated(*args, **kwargs):
        loggers['wazo_acceptance'].debug("calling %s(%s, %s)", func.__name__, args, kwargs)
        func(*args, **kwargs)
    return decorated
