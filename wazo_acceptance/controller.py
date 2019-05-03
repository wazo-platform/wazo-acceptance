# -*- coding: UTF-8 -*-
# Copyright 2014-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


from wazo_acceptance.service import prerequisite


class WazoAcceptanceController:

    def __init__(self, feature_manager):
        self._feature_manager = feature_manager

    def exec_prerequisite(self, extra_config):
        prerequisite.run(extra_config)

    def internal_features(self, internal_features):
        self._feature_manager.exec_internal_features(internal_features)
