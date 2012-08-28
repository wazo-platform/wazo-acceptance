# -*- coding: UTF-8 -*-

from xivo_lettuce.manager import context_manager


def setup():
    context_manager.add_contextnumbers_user('default', 1000, 1999)
    context_manager.add_contextnumbers_group('default', 2000, 2999)
    context_manager.add_contextnumbers_queue('default', 3000, 3999)
    context_manager.add_contextnumbers_meetme('default', 4000, 4999)
    context_manager.add_contextnumbers_incall('from-extern', 1000, 4999, 4)
