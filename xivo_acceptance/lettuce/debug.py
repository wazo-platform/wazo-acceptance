# -*- coding: utf-8 -*-
# Copyright (C) 2015-2016 Avencall
# SPDX-License-Identifier: GPL-3.0+

import logging
import requests


loggers = {
    'selenium': logging.getLogger('selenium'),
    'acceptance': logging.getLogger('acceptance'),
    'linphone': logging.getLogger('linphone'),
    'cticlient': logging.getLogger('cticlient'),
    'easyprocess': logging.getLogger('easyprocess'),
    'pyvirtualdisplay': logging.getLogger('pyvirtualdisplay')
}


def setup_logging(config):
    file_handler = logging.FileHandler(config['log_file'])

    for name, logger in loggers.iteritems():
        logger.setLevel(logging.INFO)
        for handler in logger.handlers:
            logger.removeHandler(handler)
        logger.addHandler(file_handler)
        if config['debug'].get(name):
            logger.setLevel(logging.DEBUG)

    requests.packages.urllib3.disable_warnings()


def logcall(func):
    def decorated(*args, **kwargs):
        loggers['acceptance'].debug("calling %s(%s, %s)", func.__name__, args, kwargs)
        func(*args, **kwargs)
    return decorated
