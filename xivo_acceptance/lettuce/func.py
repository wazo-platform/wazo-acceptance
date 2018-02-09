# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0+


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


def has_subsets_of_dicts(expecteds, results):
    return _all_superset_item(_list_of_dict_to_list_of_set(expecteds),
                              _list_of_dict_to_list_of_set(results))
