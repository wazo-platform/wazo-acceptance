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

import os
import logging
import subprocess

from xivo_lettuce import config


logger = logging.getLogger(__name__)


class FeatureManager(object):

    def __init__(self):
        pass

    def exec_feature(self, feature_folder, feature_file=None, interactive=False):
        feature_path = os.path.join(config._FEATURES_DIR, feature_folder)
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
                self._exec_lettuce_feature(feature_path)

    def _exec_lettuce_feature(self, feature_path):
        self._exec_sys_cmd('lettuce %s' % feature_path)

    def _exec_sys_cmd(self, cmd):
        logger.debug('Executing commmand: %s', cmd)
        subprocess.call(cmd.split(' '))
