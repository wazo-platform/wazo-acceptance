# -*- coding: UTF-8 -*-

from xivo_lettuce.manager_ws import context_manager_ws


def setup():
    context_manager_ws.update_contextnumbers_user('default', 1000, 1999)
    context_manager_ws.update_contextnumbers_group('default', 2000, 2999)
    context_manager_ws.update_contextnumbers_queue('default', 3000, 3999)
    context_manager_ws.update_contextnumbers_meetme('default', 4000, 4999)
    context_manager_ws.update_contextnumbers_incall('from-extern', 1000, 4999, 4)
