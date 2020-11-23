# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import random
import string


class Utils:
    def __init__(self, context):
        pass

    def random_string(self, length, sample=string.ascii_lowercase):
        return ''.join(random.choice(sample) for _ in range(length))
