# Copyright 2020-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import random
import string

from contextlib import contextmanager


class Utils:
    def __init__(self, context):
        pass

    def random_string(self, length, sample=string.ascii_lowercase):
        return ''.join(random.choice(sample) for _ in range(length))

    @contextmanager
    def set_token(self, client, token):
        old_token = client._token_id
        client.set_token(token)
        yield
        client.set_token(old_token)
