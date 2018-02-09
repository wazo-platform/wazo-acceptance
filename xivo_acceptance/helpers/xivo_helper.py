# -*- coding: utf-8 -*-
# Copyright (C) 2014-2015 Avencall
# SPDX-License-Identifier: GPL-3.0+

from xivo_dao.resources.infos import dao
from xivo_dao.helpers.db_utils import session_scope


def get_uuid():
    with session_scope():
        return dao.get().uuid
