# -*- coding: utf-8 -*-
from pprint import pprint

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

import unittest
from webservices.common import WSCommon



class TestSkillWebService(unittest.TestCase):
    def setUp(self):
        self._aws_skills = WSCommon('callcenter/settings/skills')

    def tearDown(self):
        pass

    def new_skill(self, skill_name, printscreen, category_name, description):
        return {
                "name": unicode(skill_name),
                "description": unicode(description),
                "printscreen": unicode(printscreen),
                "category_name": unicode(category_name)
                }

    def remove_skill(self, skill_name):
        skills = self._aws_skills.list()
        if skills is not None:
            skills_to_remove = [skill for skill in skills if skill['name'] == skill_name]
            for skill in skills_to_remove:
                self._aws_skills.delete(skill['id'])

    def test_add(self):
        skill_name = "service"
        self.remove_skill(skill_name)

        skill = self.new_skill(skill_name, "svc", "bus_test", "service skill for agents")
        self.assertTrue(self._aws_skills.simple_add(skill), "unable to add skill %s" % skill)

    def get_skill_id(self, skill_name):
        skills = self._aws_skills.list()
        if skills is not None:
            for skill in skills:
                if skill['name'] == skill_name:
                    return skill['id']

    def test_view(self):
        skill_name = "viewskill"
        self.remove_skill(skill_name)
        skill_to_add = self.new_skill(skill_name, "vsk", "bus_test", "view skill for agents test webservice")

        self._aws_skills.simple_add(skill_to_add)

        skill_id = self.get_skill_id(skill_name)

        skill = self._aws_skills.view(skill_id)

        self.assertEquals(skill_name, skill['name'])


if __name__ == '__main__':
    unittest.main()
