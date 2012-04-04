# -*- coding: utf-8 -*-

__license__ = """
    Copyright (C) 2011  Avencall

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA..
"""

import unittest, json
from webservices.common import WSCommon
from pprint import pprint


class TestAgentWebService(unittest.TestCase):
    def setUp(self):
        self._aws_agent = WSCommon('callcenter/settings/agents')

    def tearDown(self):
        pass

    def new_agent(self, number):
        return {
                "agentfeatures" : {
                    "firstname": "john",
                    "lastname" : "doe",
                    "number"   : unicode(number),
                    "passwd"   : "7789",
                    "context"  : "default",
                    "numgroup" : "1",
                    "autologoff": "0",
                    "ackcall": "no",
                    "wrapuptime": "0",
                    "enddtmf" : "*",
                    "acceptdtmf" : "#",
                 },
                "agentoptions": {
                    "musiconhold" : "default",
                    "maxlogintries":"3",
                }
        }


    def remove_agent(self, agent_number):
        agents = self._aws_agent.list()
        agents_to_remove = [agent for agent in agents if agent['number'] == agent_number]
        for agent in agents_to_remove:
            self._aws_agent.delete(agent['id'])

    def agent_exists(self, agent_number):
        agents = self._aws_agent.list()
        matching_agents = [agent for agent in agents if agent['number'] == agent_number]
        return (len(matching_agents) == 1)


    def test_add(self):
        agent_number = "5678"
        self.remove_agent(agent_number)

        agent = self.new_agent(agent_number)

        self.assertTrue(self._aws_agent.simple_add(agent))
        self.assertTrue(self.agent_exists("5678"), "agent %s is not created " % agent_number)



if __name__ == '__main__':
    unittest.main()
