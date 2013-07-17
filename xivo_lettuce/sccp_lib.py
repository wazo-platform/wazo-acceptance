class SCCPDevice(object):

    def __init__(self, mac):
        self._mac = mac

    def register(self, host, port):
        self._host = host
        self._port = port

        self._register()

    def _register(self):
        print 'Registering device %s on %s:%s' % (self._mac, self._host, self._port)

    def unregister(self):
        print 'Unregistering device %s' % self._mac
