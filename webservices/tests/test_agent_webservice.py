# -*- coding: utf-8 -*-

# Copyright (C) 2012  Avencall
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

import xivo_ws
import unittest
import common


class TestAgentWebServices(unittest.TestCase):

    def setUp(self):
        self._xivo_ws = common.xivo_server_ws

    def test_01_add_agent(self):
        agent = xivo_ws.Agent()
        agent.firstname = u'name_test_ws_add_agent'
        agent.number = u'5000'
        agent.context = u'default'
        common.delete_with_number('agents', agent.number)
        self._xivo_ws.agents.add(agent)

        self.assertEqual(common.nb_with_number('agents', agent.number), 1)

    def test_02_edit_agent(self):
        agent = common.find_with_number('agents', u'5000')[0]
        agent.firstname = u'name_test_ws_edit_agent'
        self._xivo_ws.agents.edit(agent)
        agent = common.find_with_number('agents', u'5000')[0]

        self.assertEqual(agent.firstname, u'name_test_ws_edit_agent')

    def test_03_delete_agent(self):
        common.delete_with_number('agents', u'5000')

        self.assertEqual(common.nb_with_number('agents', u'5000'), 0)

"""
    def new_agent(self, firstname, lastname, number):
        return {
                "agentfeatures": {
                    "firstname": unicode(firstname),
                    "lastname": unicode(lastname),
                    "number": unicode(number),
                    "passwd": "7789",
                    "context": "default",
                    "numgroup": "1",
                    "autologoff": "0",
                    "ackcall": "no",
                    "wrapuptime": "0",
                    "enddtmf": "*",
                    "acceptdtmf": "#",
                 },
                "agentoptions": {
                    "musiconhold": "default",
                    "maxlogintries": "3",
                }
        }

    def new_skilled_agent(self, firstname, lastname, number, skill_id, weight):
        agent = self.new_agent(firstname, lastname, number)
        agent.update({"queueskills":
                            [{
                              "weight": unicode(weight),
                              "id": unicode(skill_id)}
                             ]})
        return agent

    def remove_agent(self, agent_number):
        agents = self._aws_agent.list()
        if agents is not None:
            agents_to_remove = [agent for agent in agents if agent['number'] == agent_number]
            for agent in agents_to_remove:
                self._aws_agent.delete(agent['id'])

    def agent_exists(self, agent_number):
        agents = self._aws_agent.list()
        if agents is not None:
            matching_agents = [agent for agent in agents if agent['number'] == agent_number]
            return (len(matching_agents) == 1)

    def get_agent(self, agent_number):
        agents = self._aws_agent.list()
        if agents is not None:
            matching_agents = [agent for agent in agents if agent['number'] == agent_number]
        if len(matching_agents) == 1:
            return self._aws_agent.view(matching_agents[0]['id'])
        else:
            return None

    def assertAgentHasSkill(self, agent, skill_name):
        agent_skills = agent['queueskills']
        matching_skills = [skill for skill in agent_skills if skill['name'] == skill_name]
        self.assertTrue(len(matching_skills) == 1, 'agent has not the skill %s' % skill_name)

    def new_skill(self, skill_name):
        return {
                "name": unicode(skill_name),
                "description": "ws tests",
                "printscreen": "tst",
                "category_name": "test_skill_ws"
                }

    def add_skill_if_not_exists(self, skill_name):
        skills = self._aws_skills.list()
        if skills is None:
            skills = []
        matching_skills = [skill for skill in skills if skill['name'] == skill_name]
        if len(matching_skills) == 0:
            skill = self.new_skill(skill_name)
            self._aws_skills.add(skill)

        skills = self._aws_skills.list()
        matching_skills = [skill for skill in skills if skill['name'] == skill_name]
        return matching_skills[0]['id']

    def test_add(self):
        agent_number = "5678"
        self.remove_agent(agent_number)

        agent = self.new_agent("John test", "AddWs", agent_number)

        self.assertTrue(self._aws_agent.simple_add(agent))
        self.assertTrue(self.agent_exists(agent_number), "agent %s is not created " % agent_number)

    def test_add_with_skills(self):
        skill_name = 'test_agt_webservices'
        agent_number = "99543"
        weight = 87
        self.remove_agent(agent_number)
        skill_id = self.add_skill_if_not_exists(skill_name)

        agent = self.new_skilled_agent("Jacktest", "AddWithSkillWs", agent_number, skill_id, weight)

        self.assertTrue(self._aws_agent.simple_add(agent))

        agent_created = self.get_agent(agent_number)
        self.assertNotEqual(agent_created, None, 'agent was not properly created')
        self.assertAgentHasSkill(agent_created, skill_name)

    def test_delete_all(self):
        agent = self.new_agent('John', 'Doe', '4277')
        self._aws_agent.simple_add(agent)

        self.assertTrue(self._get_nb_of_agents() > 0)

        self._aws_agent.custom({'act': 'deleteall'})

        self.assertEqual(0, self._get_nb_of_agents())

    def _get_nb_of_agents(self):
        agent_list = self._aws_agent.list()
        if agent_list is None:
            return 0
        else:
            return len(agent_list)
"""
