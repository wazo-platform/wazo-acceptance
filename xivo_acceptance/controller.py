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


from xivo_acceptance.service import prerequisite


class XiVOAcceptanceController(object):

    def __init__(self, feature_manager):
        self._feature_manager = feature_manager

    def exec_prerequisite(self):
        prerequisite.run()

    def exec_feature(self, feature, interactive=False):
        feature_file = None
        try:
            feature_folder, feature_file = feature.split('/')
        except ValueError:
            feature_folder = feature
        except AttributeError:
            feature_folder = ''

        self._feature_manager.exec_feature(feature_folder, feature_file, interactive)
