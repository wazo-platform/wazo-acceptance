# -*- coding: utf-8 -*-

# Copyright (C) 2015 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import logging
import requests

from xivo.xivo_logging import setup_logging as xivo_setup_logging


loggers = {
    'selenium': logging.getLogger('selenium'),
    'acceptance': logging.getLogger('acceptance'),
    'linphone': logging.getLogger('linphone'),
    'cticlient': logging.getLogger('cticlient'),
    'easyprocess': logging.getLogger('easyprocess'),
    'pyvirtualdisplay': logging.getLogger('pyvirtualdisplay')
}


def setup_logging(config):
    debug = config.get('debug', {}).get('global', True)
    xivo_setup_logging(log_file=config['log_file'], foreground=True, debug=debug)
    file_handler = logging.FileHandler(config['log_file'])

    for name, logger in loggers.iteritems():
        logger.setLevel(logging.INFO)
        logger.addHandler(file_handler)
        if config['debug'].get(name):
            logger.setLevel(logging.DEBUG)

    requests.packages.urllib3.disable_warnings()


def logcall(func):
    def decorated(*args, **kwargs):
        loggers['acceptance'].debug("calling %s(%s, %s)", func.__name__, args, kwargs)
        func(*args, **kwargs)
    return decorated
