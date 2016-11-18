# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
# Copyright (C) 2016 Proformatique Inc.
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


def extract_number_and_context_from_extension(extension, default_context='default'):
    if '@' in extension:
        number, context = extension.split('@', 1)
    else:
        number = extension
        context = default_context
    return number, context


def _is_subset(subset, superset):
    return subset <= superset


def _has_superset_item(subset, supersets):
    for superset in supersets:
        if _is_subset(subset, superset):
            return True
    return False


def _all_superset_item(subsets, supersets):
    for subset in subsets:
        if not _has_superset_item(subset, supersets):
            return False
    return True


def _list_of_dict_to_list_of_set(dicts):
    return map(lambda d: set(d.iteritems()), dicts)


def _all_ordered_superset_item(subsets, supersets):
    needle = 0
    for superset in supersets:
        if needle == len(subsets):
            return True
        if _is_subset(subsets[needle], superset):
            needle += 1
    return needle == len(subsets)


def has_subsets_of_dicts(expecteds, results):
    return _all_superset_item(_list_of_dict_to_list_of_set(expecteds),
                              _list_of_dict_to_list_of_set(results))
