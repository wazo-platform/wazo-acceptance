# -*- coding: UTF-8 -*-

from xivo_lettuce.manager_ws import context_manager_ws
from xivo_lettuce.terrain import initialize, deinitialize


def main():
    initialize()
    try:
        context_manager_ws.update_contextnumbers_user('default', 1100, 1199)
    finally:
        deinitialize()


if __name__ == '__main__':
    main()
