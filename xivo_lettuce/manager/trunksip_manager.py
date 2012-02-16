# -*- coding: utf-8 -*-

import json
from lettuce.registry import world
from xivo_lettuce.common import *

WSTS = get_webservices('trunksip')


def delete_all_trunksip():
    return WSTS.clear()


def add_trunksip(name):
    jsonfilecontent = WSTS.get_json_file_content('trunksip')
    content = json.loads(jsonfilecontent)
    content['protocol']['name'] = name
    assert(WSTS.add(content))
