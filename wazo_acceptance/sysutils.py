# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import time
import datetime

from email.utils import parsedate

WAZO_SERVICE_PIDFILES = {
    'wazo-agentd': '/run/wazo-agentd/wazo-agentd.pid',
    'wazo-agid': '/run/wazo-agid/wazo-agid.pid',
    'wazo-amid': '/run/wazo-amid/wazo-amid.pid',
    'wazo-auth': '/run/wazo-auth/wazo-auth.pid',
    'wazo-call-logd': '/run/wazo-call-logd/wazo-call-logd.pid',
    'wazo-calld': '/run/wazo-calld/wazo-calld.pid',
    'wazo-chatd': '/run/wazo-chatd/wazo-chatd.pid',
    'wazo-confd': '/run/wazo-confd/wazo-confd.pid',
    'wazo-confgend': '/run/wazo-confgend/wazo-confgend.pid',
    'wazo-dird': '/run/wazo-dird/wazo-dird.pid',
    'wazo-phoned': '/run/wazo-phoned/wazo-phoned.pid',
    'wazo-plugind': '/run/wazo-plugind/wazo-plugind.pid',
    'wazo-provd': '/run/wazo-provd/wazo-provd.pid',
    'wazo-webhookd': '/run/wazo-webhookd/wazo-webhookd.pid',
    'wazo-websocketd': '/run/wazo-websocketd/wazo-websocketd.pid',
}

SERVICE_PIDFILES = {
    'asterisk': '/run/asterisk/asterisk.pid',
    'consul': '/run/consul/consul.pid',
    **WAZO_SERVICE_PIDFILES
}


class RemoteSysUtils:

    def __init__(self, ssh_client):
        self._ssh_client = ssh_client

    def path_exists(self, path):
        command = ['ls', path]
        try:
            return self._ssh_client.check_call(command) == 0
        except Exception:
            return False

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

    def is_process_running(self, pidfile):
        if not self.path_exists(pidfile):
            return False
        pid = self.get_content_file(pidfile).strip()
        return self.path_exists("/proc/%s" % pid)

    def wait_service_successfully_stopped(self, pidfile, maxtries=16, wait_secs=10):
        return self._wait_for_the_service_state(pidfile, False, maxtries, wait_secs)

    def wait_service_successfully_started(self, pidfile, maxtries=16, wait_secs=10):
        return self._wait_for_the_service_state(pidfile, True, maxtries, wait_secs)

    def _wait_for_the_service_state(self, pidfile, status, maxtries, wait_secs):
        nbtries = 0
        process_status = self.is_process_running(pidfile)
        while nbtries < maxtries and process_status != status:
            time.sleep(wait_secs)
            process_status = self.is_process_running(pidfile)
            nbtries += 1

        return process_status

    def get_pidfile_for_service_name(self, service):
        if service not in SERVICE_PIDFILES:
            assert False, 'Service %s must be implemented' % service
        return SERVICE_PIDFILES[service]

    def start_service(self, service_name):
        command = ['systemctl', 'start', service_name]
        self._ssh_client.check_call(command)

    def restart_service(self, service_name):
        command = ['systemctl', 'restart', service_name]
        self._ssh_client.check_call(command)
