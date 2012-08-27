# -*- coding: UTF-8 -*-

import xivo_ws

from lettuce.registry import world
from xivo_lettuce.terrain import _read_config
from xivo_lettuce.manager.context_manager import add_contextnumbers_user, \
    add_contextnumbers_queue, add_contextnumbers_group, \
    add_contextnumbers_meetme, add_contextnumbers_incall


def main():
    config = _read_config()
    Prerequisite(config)


class Prerequisite(object):

    def __init__(self, config):
        world.callgen_host = config.get('callgen', 'hostname')
        world.xivo_host = config.get('xivo', 'hostname')
        login = config.get('webservices_infos', 'login')
        password = config.get('webservices_infos', 'password')
        world.ws = xivo_ws.XivoServer(world.xivo_host, login, password)

        add_contextnumbers_user('default', 1000, 1999)
        add_contextnumbers_group('default', 2000, 2999)
        add_contextnumbers_queue('default', 3000, 3999)
        add_contextnumbers_meetme('default', 4000, 4999)
        add_contextnumbers_incall('from-extern', 1000, 4999, 4)


if __name__ == '__main__':
    main()
