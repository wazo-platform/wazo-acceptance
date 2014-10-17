# -*- coding: UTF-8 -*-
#
# Copyright (C) 2014 Avencall
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

from __future__ import print_function

import os
import logging
import re
import subprocess

from xivo_acceptance import config


logger = logging.getLogger(__name__)


class FeatureManager(object):

    def set_xivo_host(self, xivo_host):
        if xivo_host is None:
            return
        config_home_file = os.path.join(config._HOME_DIR, 'default')
        logger.debug('Set xivo_host %s into file %s', xivo_host, config_home_file)
        print('[xivo]\nhostname = %s' % xivo_host, file=open(config_home_file, 'w'))

    def exec_internal_features(self, features_folder, feature_file=None):
        feature_path = os.path.join(config._FEATURES_DIR, features_folder)
        if not os.path.exists(feature_path):
            logger.error('Feature folder not exist: %s', feature_path)
        else:
            if feature_file is not None:
                feature_file_path = os.path.join(feature_path, '%s.feature' % feature_file)
                if not os.path.exists(feature_file_path):
                    logger.error('Feature file not exist: %s', feature_file_path)
                else:
                    self._exec_lettuce_feature(feature_file_path)
            else:
                self.exec_external_features(feature_path)

    def exec_external_features(self, features_folder):
        for fname in os.listdir(features_folder):
            if re.match(r'.*\.feature', fname):
                logger.debug('External feature file found: %s', fname)
                feature_file_path = os.path.join(config._FEATURES_DIR, fname)
                self._exec_lettuce_feature(feature_file_path)

    def _exec_lettuce_feature(self, feature_path):
        self._exec_sys_cmd('lettuce %s' % feature_path)

    def _exec_sys_cmd(self, cmd):
        logger.debug('Executing commmand: %s', cmd)
        subprocess.call(cmd.split(' '))
