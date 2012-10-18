# -*- coding: utf-8 -*-

from lettuce import world
from xivo_lettuce.manager_ws.voicemail_manager_ws import delete_all_voicemails_with_number
from xivo_lettuce.manager_ws.user_manager_ws import delete_user_with_firstname_lastname
from xivo_lettuce.manager_ws.line_manager_ws import delete_line_with_number
from xivo_lettuce.manager_ws.incall_manager_ws import delete_incall_with_did
from xivo_ws.objects.user import User, UserLine, UserVoicemail, UserIncall


def insert_simple_user(entries):
    users = list()
    for entry in entries:
        delete_all_voicemails_with_number(entry['linenumber'])
        delete_line_with_number(entry['linenumber'], entry['context'])
        delete_user_with_firstname_lastname(entry['firstname'], entry['lastname'])
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
        delete_all_voicemails_with_number(entry['linenumber'])
        delete_line_with_number(entry['linenumber'], entry['context'])
        delete_user_with_firstname_lastname(entry['firstname'], entry['lastname'])
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
        delete_all_voicemails_with_number(entry['linenumber'])
        delete_line_with_number(entry['linenumber'], entry['context'])
        delete_user_with_firstname_lastname(entry['firstname'], entry['lastname'])
        delete_incall_with_did(entry['incall'])
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
        delete_all_voicemails_with_number(entry['linenumber'])
        delete_line_with_number(entry['linenumber'], entry['context'])
        delete_user_with_firstname_lastname(entry['firstname'], entry['lastname'])
        delete_incall_with_did(entry['incall'])
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
