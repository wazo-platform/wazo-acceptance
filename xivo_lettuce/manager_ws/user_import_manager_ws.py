# -*- coding: utf-8 -*-

import os

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from webservices.webservices import WebServicesFactory
from xivo_lettuce.manager_ws.voicemail_manager_ws import delete_voicemail_with_number
from xivo_lettuce.manager_ws.user_manager_ws import delete_user_with_firstname_lastname
from xivo_lettuce.manager_ws.line_manager_ws import delete_line_with_number
from xivo_lettuce.manager_ws.incall_manager_ws import delete_incall_with_did


CSV_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../webi/csv'))
WSU = WebServicesFactory('ipbx/pbx_settings/users')


def insert_simple_user(entries):
    data = {'users': []}
    for entry in entries:
        delete_voicemail_with_number(entry['linenumber'])
        delete_line_with_number(entry['linenumber'], 'default')
        delete_user_with_firstname_lastname(entry['firstname'], entry['lastname'])
        user = {
            'entityid': 1,
            'firstname': entry['firstname'],
            'lastname': entry['lastname'],
            'language': 'en_US',
            'phonenumber': entry['linenumber'],
            'context': 'default',
            'protocol': 'sip',
            'mobilephonenumber': '0033123456789'
         }
        data['users'].append(user)

    csv_dir = os.path.join(CSV_DIR, 'user')
    tpl_processor = _TemplatesProcessor(csv_dir, data)
    tpl_processor.generate_files()

    data_post = tpl_processor.read_file('import_user.csv')

    response = WSU.custom({'act': 'import'}, data_post)
    assert(response.code == 200)


def insert_adv_user_with_mevo(entries):
    data = {'users': []}
    for entry in entries:
        delete_voicemail_with_number(entry['linenumber'])
        delete_line_with_number(entry['linenumber'], 'default')
        delete_user_with_firstname_lastname(entry['firstname'], entry['lastname'])
        user = {
            'entityid': 1,
            'firstname': entry['firstname'],
            'lastname': entry['lastname'],
            'language': 'en_US',
            'phonenumber': entry['linenumber'],
            'context': 'default',
            'protocol': 'sip',
            'mobilephonenumber': '0033123456789',
            'mailbox': entry['voicemail'],
            'mailbox_passwd': '1234',
            'mailbox_mail': 'dev@avencall.com'
         }
        data['users'].append(user)

    csv_dir = os.path.join(CSV_DIR, 'user_with_mevo')
    tpl_processor = _TemplatesProcessor(csv_dir, data)
    tpl_processor.generate_files()

    data_post = tpl_processor.read_file('import_user_with_mevo.csv')

    response = WSU.custom({'act': 'import'}, data_post)
    assert(response.code == 200)


def insert_adv_user_with_incall(entries):
    data = {'users': []}
    for entry in entries:
        delete_voicemail_with_number(entry['linenumber'])
        delete_line_with_number(entry['linenumber'], 'default')
        delete_user_with_firstname_lastname(entry['firstname'], entry['lastname'])
        delete_incall_with_did(entry['incall'])
        user = {
            'entityid': 1,
            'firstname': entry['firstname'],
            'lastname': entry['lastname'],
            'language': 'en_US',
            'phonenumber': entry['linenumber'],
            'context': 'default',
            'protocol': 'sip',
            'mobilephonenumber': '0033123456789',
            'incallexten': entry['incall'],
            'incallcontext': 'from-extern'
         }
        data['users'].append(user)

    csv_dir = os.path.join(CSV_DIR, 'user_with_incall')
    tpl_processor = _TemplatesProcessor(csv_dir, data)
    tpl_processor.generate_files()

    data_post = tpl_processor.read_file('import_user_with_incall.csv')

    response = WSU.custom({'act': 'import'}, data_post)
    assert(response.code == 200)


def insert_adv_user_full_infos(entries):
    data = {'users': []}
    for entry in entries:
        delete_voicemail_with_number(entry['voicemail'])
        delete_line_with_number(entry['linenumber'], 'default')
        delete_user_with_firstname_lastname(entry['firstname'], entry['lastname'])
        delete_incall_with_did(entry['incall'])
        user = {
            'entityid': 1,
            'firstname': entry['firstname'],
            'lastname': entry['lastname'],
            'language': 'en_US',
            'outcallerid': 'outcallerid',
            'enableclient': True,
            'username': entry['firstname'].lower(),
            'password': 'password',
            'profileclient': 'client',
            'enablehint': True,
            'agentnumber': '2000',
            'mobilephonenumber': '0033123456789',
            'bosssecretary': '',
            'phonenumber': entry['linenumber'],
            'context': 'default',
            'protocol': 'sip',
            'linename': '123456',
            'linesecret': '654321',
            'incallexten': entry['incall'],
            'incallcontext': 'from-extern',
            'mailbox': entry['voicemail'],
            'mailbox_passwd': '1234',
            'mailbox_mail': 'dev@avencall.com'
         }
        data['users'].append(user)

    csv_dir = os.path.join(CSV_DIR, 'user_full_infos')
    tpl_processor = _TemplatesProcessor(csv_dir, data)
    tpl_processor.generate_files()

    data_post = tpl_processor.read_file('import_user_full_infos.csv')

    response = WSU.custom({'act': 'import'}, data_post)
    assert(response.code == 200)


class _TemplatesProcessor(object):
    _TEMPLATE_SUFFIX = '.tpl'
    _TEMPLATE_SUFFIX_LENGTH = len(_TEMPLATE_SUFFIX)

    def __init__(self, directory, context):
        self._directory = directory
        self._context = context
        self._environment = Environment(loader=FileSystemLoader(directory),
                                        undefined=StrictUndefined)

    def generate_files(self):
        for tpl_filename in self._list_template_filenames():
            self._generate_file_from_template(tpl_filename)

    def read_file(self, filename):
        abs_filename = os.path.join(self._directory, filename)
        with open(abs_filename) as fobj:
            return fobj.read()

    def _list_template_filenames(self):
        for filename in os.listdir(self._directory):
            if self._is_template_filename(filename):
                yield filename

    def _is_template_filename(self, filename):
        return filename.endswith(self._TEMPLATE_SUFFIX)

    def _generate_file_from_template(self, tpl_filename):
        filename = self._get_template_destination(tpl_filename)
        template = self._environment.get_template(tpl_filename)
        template.stream(self._context).dump(filename)

    def _get_template_destination(self, tpl_filename):
        filename = tpl_filename[:-self._TEMPLATE_SUFFIX_LENGTH]
        return os.path.join(self._directory, filename)
