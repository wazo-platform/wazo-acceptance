# -*- coding: UTF-8 -*-

import socket

from lettuce import world
from xivo_lettuce.manager_ws import context_manager_ws, trunksip_manager_ws
from xivo_lettuce.terrain import initialize, deinitialize


def main():
    initialize()
    try:
        context_manager_ws.update_contextnumbers_user('default', 1000, 1999)
        context_manager_ws.update_contextnumbers_queue('default', 3000, 3999)
        context_manager_ws.update_contextnumbers_incall('from-extern', 1000, 4999, 4)

        callgen_ip = socket.gethostbyname(world.callgen_host)
        print 'Adding default SIP trunk'
        trunksip_manager_ws.add_or_replace_trunksip(callgen_ip, 'to_incall', 'from-extern')
    finally:
        deinitialize()


if __name__ == '__main__':
    main()
