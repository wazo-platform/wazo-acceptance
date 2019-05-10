# -*- coding: utf-8 -*-
# Copyright 2017-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import requests

from behave import then

from hamcrest import (
    assert_that,
    equal_to,
    not_,
)


@then('"{method}" "{url_path}" does not answer 404')
def then_url_does_not_answer_404(context, method, url_path):
    host = context.wazo_config['wazo_host']
    url = 'https://{host}{url_path}'.format(host=host, url_path=url_path)
    response = requests.request(method, url, verify=False)
    assert_that(response.status_code, not_(equal_to(404)), url_path)
