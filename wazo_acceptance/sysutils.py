# Copyright 2013-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import time
import datetime

from email.utils import parsedate


class RemoteSysUtils:

    def __init__(self, ssh_client):
        self._ssh_client = ssh_client

    def path_exists(self, path):
        command = ['ls', path]
        return self._ssh_client.call(command) == 0

    def dir_is_empty(self, path):
        command = ['ls', '-1A', path, '|', 'wc', '-l']
        return self._ssh_client.out_call(command).strip() == '0'

    def get_list_file(self, path):
        command = ['ls', path]
        return self._ssh_client.out_call(command)

    def file_owned_by_user(self, path, owner):
        command = ['stat', '-c', '%U', path]
        return self._ssh_client.out_call(command).strip() == owner

    def file_owned_by_group(self, path, owner):
        command = ['stat', '-c', '%G', path]
        return self._ssh_client.out_call(command).strip() == owner

    def get_content_file(self, path):
        command = ['cat', path]
        return self._ssh_client.out_call(command)

    def write_content_file(self, path, content):
        command = ['echo', '-en', f"'{content}'", '>', path]
        self._ssh_client.check_call(command)

    def wazo_current_datetime(self):
        # The main problem here is the timezone: `date` must give us the date in
        # localtime, because the log files are using localtime dates.
        command = ['date', '-R']
        output = self.output_command(command).strip()
        date = parsedate(output)
        return datetime.datetime(*date[:6])

    def send_command(self, command, check=True):
        if check:
            res = self._ssh_client.check_call(command) == 0
        else:
            res = self._ssh_client.call(command) == 0
        time.sleep(1)
        return res

    def output_command(self, command):
        res = self._ssh_client.out_call(command)
        time.sleep(1)
        return res

    def is_process_running(self, service_name):
        command = ['systemctl', 'show', '--property', 'ActiveState', '--value', service_name]
        output = self._ssh_client.out_call(command).strip()
        if output == 'inactive':
            return False
        elif output == 'active':
            return True
        raise Exception(f'Invalid output: {output}')

    def process_priority(self, service_name):
        pid = self._get_pid(service_name)
        command = ['cut', '-d" "', '-f18', f'/proc/{pid}/stat']
        return self._ssh_client.out_call(command).strip()

    def _get_pid(self, service_name):
        command = ['systemctl', 'show', '--property', 'MainPID', '--value', service_name]
        pid = self._ssh_client.out_call(command).strip()
        if not pid:
            raise Exception(f'Unknown PID for {service_name}')
        return pid

    def process_limitnofile(self, service_name):
        command = ['systemctl', 'show', '--property', 'LimitNOFILE', '--value', service_name]
        return self._ssh_client.out_call(command).strip()

    def start_service(self, service_name):
        command = ['systemctl', 'start', service_name]
        self._ssh_client.check_call(command)

    def restart_service(self, service_name):
        command = ['systemctl', 'restart', service_name]
        self._ssh_client.check_call(command)

    def reload_service(self, service_name):
        command = ['systemctl', 'reload', service_name]
        self._ssh_client.check_call(command)

    def get_mails(self, since=None):
        command = ['cat', '/var/spool/mail/root']
        output = self.output_command(command)
        mails = self._extract_mails(output)
        if since:
            since = since.replace(microsecond=0)  # mail doesn't have microsecond
            mails = [mail for mail in mails if mail['Date'] >= since]
        return mails

    def _extract_mails(self, content):
        mails = []
        mails_raw = content.split('Return-Path:')[1:]
        for mail_raw in mails_raw:
            mail_raw = f'Return-Path:{mail_raw}'
            mail = {'body': ''}

            headers_raw, body = mail_raw.split('\n\n', 1)
            headers_raw = headers_raw.replace('\n        ', ' ')  # wrap multi-lines
            mail['body'] = body.strip()
            for header_raw in headers_raw.split('\n'):
                key, value = header_raw.split(':', 1)
                value = value.strip()
                if key == 'Date':
                    value = value.split(',')[1].strip()
                    value = datetime.datetime.strptime(value, '%d %b %Y %H:%M:%S %z')
                mail[key] = value
            mails.append(mail)
        return mails
