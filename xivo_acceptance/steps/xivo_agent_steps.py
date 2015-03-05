# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from lettuce import step
from xivo_acceptance.lettuce import logs


@step(u'Then I see that xivo-agent has reconnected to the AMI in the logs')
def then_i_see_that_xivo_agent_has_reconnected_to_the_ami_in_the_logs(step):
    assert logs.search_str_in_xivo_agent_log("Connecting AMI client to localhost:5038")
