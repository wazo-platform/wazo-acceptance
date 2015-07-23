# -*- coding: utf-8 -*-

# Copyright (C) 2014-2015 Avencall
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

from xivo_acceptance.action.webi import directory as directory_action_webi


def configure_internal_directory():
    directory_action_webi.add_or_replace_directory(
        name='internal',
        uri='http://localhost:9487',
        direct_match='userfeatures.firstname,userfeatures.lastname',
        reverse_match='',
        fields={'firstname': 'userfeatures.firstname',
                'lastname': 'userfeatures.lastname',
                'phone': 'extensions.exten'}
    )
