import os

from subprocess import Popen
from subprocess import PIPE
from tempfile import NamedTemporaryFile


class SipPhone(object):

    _CONFIG_FILE_CONTENT = '''
[sip]
sip_port=%s
'''

    def __init__(self, sip_name, sip_passwd, port):
        self._port = port
        self._sip_name = sip_name
        self._sip_passwd = sip_passwd

        self._create_config_file()
        self._session = Popen('linphonec -c %s' % self._config_file, stdin=PIPE)

    def call(self, exten):
        self._send_command('call %s' % exten)

    def register(self):
        params = {
            'sip_name': self._sip_name,
            'hostname': self._hostname,
            'sip_passwd': self._passwd,
        }
        command = 'register sip:%(sip_name)s:%(hostname) %(sip_name)s %(sip_passwd)' % params
        self._send_command(command)

    def unregister(self):
        self._send_command('unregister')

    def quit(self):
        self._send_command('quit')

    def _send_command(self, command):
        self._session.stdin.write(command)

    def _create_config_file(self):
        with NamedTemporaryFile(delete=False) as f:
            self._config_file = f.name
            f.write(self._CONFIG_FILE_CONTENT % self._port)

    def __del__(self):
        self.unregister()
        self.quit()
        self._session.wait()
        if os.path.exists(self._config_file):
            os.unlink(self._config_file)
