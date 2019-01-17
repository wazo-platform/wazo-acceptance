# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_acceptance.lettuce import common


def webi_exec_commonconf():
    common.open_url('commonconf')
