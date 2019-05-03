# -*- coding: UTF-8 -*-
# Copyright 2014-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import os
import subprocess


logger = logging.getLogger(__name__)


class FeatureManager:

    def __init__(self, config):
        self.config = config

    def exec_internal_features(self, internal_features):
        feature_path = os.path.join(self.config['features_dir'], internal_features)
        feature_file_path = '%s.feature' % feature_path

        if os.path.exists(feature_file_path):
            self._exec_behave_feature(feature_file_path)
        elif os.path.isdir(feature_path):
            self._exec_behave_feature(feature_path)
        else:
            raise Exception('Unknown path: %s', feature_path)

    def _exec_behave_feature(self, feature_path):
        cmd = 'behave {feature_path} --junit --verbosity=3 --junit={output_dir}'.format(
            feature_path=feature_path,
            output_dir=self.config['output_dir'],
        )
        self._exec_sys_cmd(cmd)

    def _exec_sys_cmd(self, cmd):
        logger.debug('Executing commmand: %s', cmd)
        subprocess.call(cmd.split(' '))
