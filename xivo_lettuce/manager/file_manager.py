# -*- coding: UTF-8 -*-

import os

from lettuce.registry import world
from xivo_lettuce import common as com
from selenium.common.exceptions import NoSuchElementException

SOUND_REC_PATH = '/usr/share/asterisk/sounds/recordings'


def check_recordings_file(filename):
    return(os.access(os.path.join(SOUND_REC_PATH, filename), os.R_OK))
