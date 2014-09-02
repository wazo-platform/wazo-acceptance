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

USERS_URL = 'users'


def all_users():
    return world.confd_utils_1_1.rest_get(USERS_URL)


def get_lines_associated_to_a_user(userid):
    return world.confd_utils_1_1.rest_get('%s/%s/user_links' % (USERS_URL, userid))


def get_user(userid):
    return world.confd_utils_1_1.rest_get('%s/%s' % (USERS_URL, userid))


def user_search(search):
    params = {'q': search}
    return world.confd_utils_1_1.rest_get(USERS_URL, params=params)


def create_user(parameters):
    return world.confd_utils_1_1.rest_post(USERS_URL, parameters)


def update_user(userid, parameters):
    return world.confd_utils_1_1.rest_put('%s/%s' % (USERS_URL, userid), parameters)


def delete_user(userid):
    return world.confd_utils_1_1.rest_delete('%s/%s' % (USERS_URL, userid))
