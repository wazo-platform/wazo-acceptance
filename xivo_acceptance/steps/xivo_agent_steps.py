# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0+

from lettuce import step
from xivo_acceptance.lettuce import logs


@step(u'Then I see that xivo-agent has reconnected to the AMI in the logs')
def then_i_see_that_xivo_agent_has_reconnected_to_the_ami_in_the_logs(step):
    assert logs.search_str_in_xivo_agent_log("Connecting AMI client to localhost:5038")
