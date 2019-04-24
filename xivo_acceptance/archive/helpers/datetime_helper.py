# -*- coding: utf-8 -*-
# Copyright (C) 2014 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import all_of
from hamcrest import greater_than
from hamcrest import less_than


def close_to(target, delta):
    minimum = target - delta
    maximum = target + delta
    return all_of(greater_than(minimum),
                  less_than(maximum))
