# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import requests

from hamcrest import (
    assert_that,
    not_,
)
from lettuce import step, world


@step(u'Then "([^"]*)" "([^"]*)" does not answer 404')
def then_group1_group2_does_not_answer_404(step, method, url_path):
    url = 'https://{host}{url_path}'.format(host=world.config['xivo_host'], url_path=url_path)
    response = requests.request(method, url, verify=False)
    assert_that(response.status_code, not_(404))
