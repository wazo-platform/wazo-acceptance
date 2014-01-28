# -*- coding: utf-8 -*-

# Copyright (C) 2012-2014 Avencall
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

from lettuce.registry import world

CTI_PROFILES_URL = 'cti_profiles'
USERS_URL = 'users'


def all_profiles():
    return world.restapi_utils_1_1.rest_get(CTI_PROFILES_URL)


def get_cti_profile(profileid):
    return world.restapi_utils_1_1.rest_get('%s/%s' % (CTI_PROFILES_URL, profileid))


def associate_profile_to_user(cti_profile_id, user_id):
    return world.restapi_utils_1_1.rest_put('%s/%s/cti' % (USERS_URL, user_id), {'cti_profile_id': cti_profile_id})


def get_cti_profile_for_user(userid):
    return world.restapi_utils_1_1.rest_get('%s/%s/cti' % (USERS_URL, userid))


def enable_cti_for_user(user_id):
    return world.restapi_utils_1_1.rest_put('%s/%s/cti' % (USERS_URL, user_id), {'enabled': True})
