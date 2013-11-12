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

from xivo_acceptance.helpers import user_helper, incall_helper
from xivo_ws.objects.user import User, UserLine, UserVoicemail, UserIncall


def insert_simple_user(entries):
    users = list()
    for entry in entries:
        mailbox = entry.get('linenumber', None)
        exten = entry.get('linenumber', None)
        context = entry.get('context', None)
        user_helper.delete_user_line_extension_voicemail(entry['firstname'],
                                                              entry['lastname'],
                                                              exten=exten,
                                                              context=context,
                                                              mailbox=mailbox)
        user = User()
        user.firstname = entry['firstname']
        user.lastname = entry['lastname']
        if 'enable_transfer' in entry:
            user.enable_transfer = entry['enable_transfer']
        user.line = UserLine()
        user.line.context = entry['context']
        user.line.number = entry['linenumber']
        users.append(user)

    world.ws.users.import_(users)


def insert_adv_user_with_mevo(entries):
    users = list()
    for entry in entries:
        mailbox = entry.get('linenumber', None)
        exten = entry.get('linenumber', None)
        context = entry.get('context', None)
        user_helper.delete_user_line_extension_voicemail(entry['firstname'],
                                                              entry['lastname'],
                                                              exten=exten,
                                                              context=context,
                                                              mailbox=mailbox)
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
        mailbox = entry.get('linenumber', None)
        exten = entry.get('linenumber', None)
        context = entry.get('context', None)
        user_helper.delete_user_line_extension_voicemail(entry['firstname'],
                                                              entry['lastname'],
                                                              exten=exten,
                                                              context=context,
                                                              mailbox=mailbox)
        incall_helper.delete_incalls_with_did(entry['incall'])
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
        mailbox = entry.get('linenumber', None)
        exten = entry.get('linenumber', None)
        context = entry.get('context', None)
        user_helper.delete_user_line_extension_voicemail(entry['firstname'],
                                                              entry['lastname'],
                                                              exten=exten,
                                                              context=context,
                                                              mailbox=mailbox)
        incall_helper.delete_incalls_with_did(entry['incall'])
        user = User()
        user.firstname = entry['firstname']
        user.lastname = entry['lastname']
        user.language = 'fr_FR'
        user.line = UserLine()
        user.line.context = entry['context']
        user.line.number = entry['linenumber']
        user.line.secret = entry.get('linesecret', '')
        user.voicemail = UserVoicemail()
        user.voicemail.name = '%s %s' % (entry['firstname'], entry['lastname'])
        user.voicemail.number = entry['voicemail']
        user.incall = UserIncall()
        user.incall.exten = entry['incall']
        user.incall.context = 'from-extern'
        users.append(user)

    world.ws.users.import_(users)
