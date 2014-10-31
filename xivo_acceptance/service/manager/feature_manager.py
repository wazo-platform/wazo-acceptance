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
import re
import subprocess

from lettuce.registry import world


logger = logging.getLogger(__name__)


class FeatureManager(object):

    def set_xivo_host(self, xivo_host):
        if xivo_host:
            logger.debug('Set xivo_host %s', xivo_host)
            os.environ["XIVO_HOST"] = xivo_host

    def exec_internal_features(self, internal_features):
        feature_path = os.path.join(world.config.features_dir, internal_features)
        feature_file_path = '%s.feature' % feature_path

        if os.path.exists(feature_file_path):
            self._exec_lettuce_feature(feature_file_path)
        elif os.path.isdir(feature_path):
            self.exec_external_features(feature_path)
        else:
            raise Exception('Unknown path: %s', feature_path)

    def exec_external_features(self, feature_path):
        for feature in self._files_in(feature_path):
            if re.match(r'.*\.feature', feature):
                feature_file_path = os.path.join(world.config.features_dir, feature)
                logger.debug('External feature file found: %s', feature_file_path)
                self._exec_lettuce_feature(feature_file_path)

    def _files_in(self, directory):
        for dir, _, files in os.walk(directory):
            for file in files:
                yield '{dir}/{file}'.format(dir=dir, file=file)

    def _exec_lettuce_feature(self, feature_path):
        self._exec_sys_cmd('lettuce %s' % feature_path)

    def _exec_sys_cmd(self, cmd):
        logger.debug('Executing commmand: %s', cmd)
        subprocess.call(cmd.split(' '))
