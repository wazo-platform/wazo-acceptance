# -*- coding: UTF-8 -*-

import socket
from lettuce import world
from xivo_lettuce.manager_ws import context_manager_ws, trunksip_manager_ws
from xivo_lettuce.terrain import initialize_from_config


def main():
    initialize_from_config()
    context_manager_ws.update_contextnumbers_user('default', 1000, 1100)

    callgen_ip = socket.gethostbyname(world.callgen_host)
    trunksip_manager_ws.add_or_replace_trunksip(callgen_ip, 'to_default', 'default')


if __name__ == '__main__':
    main()
