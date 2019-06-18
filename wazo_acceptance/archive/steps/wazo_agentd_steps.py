# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import step
from xivo_acceptance.lettuce import logs


@step(u'Then I see that wazo-agentd has reconnected to the AMI in the logs')
def then_i_see_that_wazo_agentd_has_reconnected_to_the_ami_in_the_logs(step):
    assert logs.search_str_in_wazo_agentd_log("Connecting AMI client to localhost:5038")
