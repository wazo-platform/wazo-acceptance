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

import unittest
from copy import copy

from .. import func


class TestFunc(unittest.TestCase):

    def test_compare_list_of_dict_perfect_match(self):
        expected = [{u'E-mail': u'',
                     u'Entreprise': u'',
                     u'Mobile': u'',
                     u'Nom': u'Emmett Brown',
                     u'Num\xe9ro': u'0601020304',
                     u'Source': u''}]
        result = [{u'E-mail': u'',
                   u'Entreprise': u'',
                   u'Mobile': u'',
                   u'Nom': u'Emmett Brown',
                   u'Num\xe9ro': u'0601020304',
                   u'Source': u''}]

        self.assertTrue(func.has_subsets_of_dicts(expected, result))

    def test_compare_list_of_dict_more_than_expected(self):
        expected = [{u'E-mail': u'',
                     u'Entreprise': u'',
                     u'Mobile': u'',
                     u'Nom': u'Emmett Brown',
                     u'Num\xe9ro': u'0601020304',
                     u'Source': u''}]
        result = [
            {u'E-mail': u'',
             u'Entreprise': u'',
             u'Mobile': u'',
             u'Nom': u'Emmett Brown',
             u'Num\xe9ro': u'0601020304',
             u'Source': u''},
            {u'E-mail': u'',
             u'Entreprise': u'',
             u'Mobile': u'',
             u'Nom': u'NOT Emmett Brown',
             u'Num\xe9ro': u'77777',
             u'Source': u''},
        ]

        self.assertTrue(func.has_subsets_of_dicts(expected, result))

    def test_compare_list_of_dict_partial_match(self):
        result = [{u'E-mail': u'',
                   u'Entreprise': u'',
                   u'Mobile': u'',
                   u'Nom': u'Emmett Brown',
                   u'Num\xe9ro': u'0601020304',
                   u'Source': u''}]
        expected = [
            {u'E-mail': u'',
             u'Entreprise': u'',
             u'Mobile': u'',
             u'Nom': u'Emmett Brown',
             u'Num\xe9ro': u'0601020304',
             u'Source': u''},
            {u'E-mail': u'',
             u'Entreprise': u'',
             u'Mobile': u'',
             u'Nom': u'NOT Emmett Brown',
             u'Num\xe9ro': u'77777',
             u'Source': u''},
        ]

        self.assertFalse(func.has_subsets_of_dicts(expected, result))

    def test_compare_list_of_dict_empty(self):
        self.assertTrue(func.has_subsets_of_dicts([], []))

    def test_compare_list_of_dict_many_different_order(self):
        expected = [
            {u'E-mail': u'',
             u'Entreprise': u'',
             u'Mobile': u'',
             u'Nom': u'Emmett Brown',
             u'Num\xe9ro': u'0601020304',
             u'Source': u''},
            {u'E-mail': u'',
             u'Entreprise': u'',
             u'Mobile': u'',
             u'Nom': u'NOT Emmett Brown',
             u'Num\xe9ro': u'77777',
             u'Source': u''},
        ]
        result = copy(expected)
        result.reverse()

        self.assertTrue(func.has_subsets_of_dicts(expected, result))
