# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0+

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
