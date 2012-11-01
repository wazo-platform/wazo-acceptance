# -*- coding: utf-8 -*-

from lettuce import world


def delete_incalls_with_did(incall_did):
    incalls = world.ws.incalls.search_by_number(incall_did)
    for incall in incalls:
        world.ws.incalls.delete(incall.id)
