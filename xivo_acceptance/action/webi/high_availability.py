# -*- coding: utf-8 -*-
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0+

from xivo_acceptance.lettuce import common
from xivo_acceptance.lettuce.form import submit, input, select


def set_ha_config(mode, remote=None):
    common.open_url('ha')
    type_ha_config(mode, remote)
    submit.submit_form()


def set_ha_config_ignore_errors(mode, remote=None):
    common.open_url('ha')
    type_ha_config(mode, remote)
    submit.submit_form_ignore_errors()


def type_ha_config(mode, remote=None):
    select.set_select_field_with_label("Type of this node", mode)
    if remote:
        input.set_text_field_with_label("Remote address", remote)
