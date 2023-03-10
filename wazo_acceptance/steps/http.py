# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
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


@then('"{method}" "{url_path}" eventually receive the answer 429 instead of "{status_code}"')
def then_url_answer_429(context, method, url_path, status_code):
    host = context.wazo_config['wazo_host']
    url = f'https://{host}{url_path}'
    response = requests.request(method, url, verify=False)
    assert_that(response.status_code, equal_to(int(status_code)))

    for _ in range(1000):
        response = requests.request(method, url, verify=False)
        if response.status_code == 429:
            return

    assert_that(response.status_code, equal_to(429))
