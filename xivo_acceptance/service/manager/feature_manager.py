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

import logging
import os
import subprocess


logger = logging.getLogger(__name__)


class FeatureManager(object):

    def __init__(self, config):
        self.config = config

    def exec_internal_features(self, internal_features):
        feature_path = os.path.join(self.config['features_dir'], internal_features)
        feature_file_path = '%s.feature' % feature_path

        if os.path.exists(feature_file_path):
            self._exec_lettuce_feature(feature_file_path)
        elif os.path.isdir(feature_path):
            self._exec_lettuce_feature(feature_path)
        else:
            raise Exception('Unknown path: %s', feature_path)

    def _exec_lettuce_feature(self, feature_path):
        cmd = 'lettuce {feature_path} --with-xunit --verbosity=3 --xunit-file={output_dir}/xunit-tests.xml'.format(feature_path=feature_path,
                                                                                                                   output_dir=self.config['output_dir'])
        self._exec_sys_cmd(cmd)

    def _exec_sys_cmd(self, cmd):
        logger.debug('Executing commmand: %s', cmd)
        subprocess.call(cmd.split(' '))
