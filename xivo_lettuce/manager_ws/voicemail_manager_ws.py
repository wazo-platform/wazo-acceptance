# -*- coding: utf-8 -*-

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


def delete_voicemail_with_id(voicemail_id):
    world.ws.voicemails.delete(voicemail_id)


def delete_voicemails_with_number(number):
    for voicemail in _search_voicemails_with_number(number):
        delete_voicemail_with_id(voicemail.id)


def _search_voicemails_with_number(number):
    return world.ws.voicemails.search_by_number(number)
