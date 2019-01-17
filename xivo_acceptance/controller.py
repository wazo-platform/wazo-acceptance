# -*- coding: UTF-8 -*-
# Copyright (C) 2014-2016 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later


from xivo_acceptance.service import prerequisite


class XiVOAcceptanceController(object):

    def __init__(self, feature_manager):
        self._feature_manager = feature_manager

    def exec_prerequisite(self, extra_config):
        prerequisite.run(extra_config)

    def internal_features(self, internal_features):
        self._feature_manager.exec_internal_features(internal_features)
