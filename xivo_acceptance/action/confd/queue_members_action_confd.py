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
from lettuce.registry import world

AGENT_QUEUE_MEMBERS_PATH = 'queues/%s/memberships/agents/%s'


def get_agent_queue_association(queue_member):
    return world.confd_utils_1_1.rest_get(AGENT_QUEUE_MEMBERS_PATH % (queue_member['queue_id'], queue_member['agent_id']))


def edit_agent_queue_association(queue_member):
    return world.confd_utils_1_1.rest_put(AGENT_QUEUE_MEMBERS_PATH % (queue_member['queue_id'], queue_member['agent_id']),
                                            {'penalty': queue_member['penalty']})
