# -*- coding: UTF-8 -*-

from xivo_lettuce.common import open_url
from xivo_lettuce.checkbox import Checkbox
from xivo_lettuce import form


def enable_live_reload():
    _toggle_live_reload('enable')


def disable_live_reload():
    _toggle_live_reload('disable')


def _toggle_live_reload(state):
    open_url('general_settings')
    option = Checkbox.from_label('Live reload configuration')
    if state == 'enable':
        option.check()
    else:
        option.uncheck()
    form.submit_form()
