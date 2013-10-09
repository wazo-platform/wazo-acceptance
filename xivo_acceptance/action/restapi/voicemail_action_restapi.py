# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Avencall
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

from lettuce import world

VOICEMAIL_URL = 'voicemails'


def get_voicemail(voicemail_id):
    return world.restapi_utils_1_1.rest_get('/%s/%s' % (VOICEMAIL_URL, voicemail_id))


def voicemail_list(parameters={}):
    return world.restapi_utils_1_1.rest_get('%s' % VOICEMAIL_URL, params=parameters)
