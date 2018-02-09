# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0+

from xivo_acceptance.lettuce.form.checkbox import Checkbox
from xivo_acceptance.lettuce import common, form


def enable_live_reload():
    _toggle_live_reload('enable')


def disable_live_reload():
    _toggle_live_reload('disable')


def _toggle_live_reload(state):
    common.open_url('general_settings')
    option = Checkbox.from_label('Live reload configuration')
    if state == 'enable':
        option.check()
    else:
        option.uncheck()
    form.submit.submit_form()
