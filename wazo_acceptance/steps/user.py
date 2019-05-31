# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import random
import string

from behave import given


def random_string(length, sample=string.ascii_lowercase):
    return ''.join(random.choice(sample) for _ in range(length))


@given('there is an authentication user')
def given_there_is_a_user(context):
    context.username = random_string(10)
    context.password = random_string(10, sample=string.printable)

    body = {
        'firstname': random_string(10),
        'username': context.username,
        'password': context.password,
    }
    context.helpers.user.create(body)
