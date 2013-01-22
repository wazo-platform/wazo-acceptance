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
from xivo_lettuce.manager_ws.voicemail_manager_ws import delete_voicemails_with_number
from xivo_lettuce.manager_ws.user_manager_ws import delete_users_with_firstname_lastname
from xivo_lettuce.manager_ws.line_manager_ws import delete_lines_with_number
from xivo_lettuce.manager_ws.incall_manager_ws import delete_incalls_with_did
from xivo_ws.objects.user import User, UserLine, UserVoicemail, UserIncall


def insert_simple_user(entries):
    users = list()
    for entry in entries:
        delete_voicemails_with_number(entry['linenumber'])
        delete_lines_with_number(entry['linenumber'], entry['context'])
        delete_users_with_firstname_lastname(entry['firstname'], entry['lastname'])
        user = User()
        user.firstname = entry['firstname']
        user.lastname = entry['lastname']
        user.line = UserLine()
        user.line.context = entry['context']
        user.line.number = entry['linenumber']
        users.append(user)

    world.ws.users.import_(users)


def insert_adv_user_with_mevo(entries):
    users = list()
    for entry in entries:
        delete_voicemails_with_number(entry['linenumber'])
        delete_lines_with_number(entry['linenumber'], entry['context'])
        delete_users_with_firstname_lastname(entry['firstname'], entry['lastname'])
        user = User()
        user.firstname = entry['firstname']
        user.lastname = entry['lastname']
        user.language = 'fr_FR'
        user.line = UserLine()
        user.line.context = entry['context']
        user.line.number = entry['linenumber']
        user.voicemail = UserVoicemail()
        user.voicemail.name = '%s %s' % (entry['firstname'], entry['lastname'])
        user.voicemail.number = entry['voicemail']
        users.append(user)

    world.ws.users.import_(users)


def insert_adv_user_with_incall(entries):
    users = list()
    for entry in entries:
        delete_voicemails_with_number(entry['linenumber'])
        delete_lines_with_number(entry['linenumber'], entry['context'])
        delete_users_with_firstname_lastname(entry['firstname'], entry['lastname'])
        delete_incalls_with_did(entry['incall'])
        user = User()
        user.firstname = entry['firstname']
        user.lastname = entry['lastname']
        user.line = UserLine()
        user.line.context = entry['context']
        user.line.number = entry['linenumber']
        user.incall = UserIncall()
        user.incall.exten = entry['incall']
        user.incall.context = 'from-extern'
        users.append(user)

    world.ws.users.import_(users)


def insert_adv_user_full_infos(entries):
    users = list()
    for entry in entries:
        delete_voicemails_with_number(entry['linenumber'])
        delete_lines_with_number(entry['linenumber'], entry['context'])
        delete_users_with_firstname_lastname(entry['firstname'], entry['lastname'])
        delete_incalls_with_did(entry['incall'])
        user = User()
        user.firstname = entry['firstname']
        user.lastname = entry['lastname']
        user.language = 'fr_FR'
        user.line = UserLine()
        user.line.context = entry['context']
        user.line.number = entry['linenumber']
        user.voicemail = UserVoicemail()
        user.voicemail.name = '%s %s' % (entry['firstname'], entry['lastname'])
        user.voicemail.number = entry['voicemail']
        user.incall = UserIncall()
        user.incall.exten = entry['incall']
        user.incall.context = 'from-extern'
        users.append(user)

    world.ws.users.import_(users)
