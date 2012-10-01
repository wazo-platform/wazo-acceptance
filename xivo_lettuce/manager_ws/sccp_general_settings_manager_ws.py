# -*- coding: utf-8 -*-

from contextlib import contextmanager
from lettuce import world
from xivo_ws import SCCPGeneralSettings

@contextmanager
def sccp_settings():
    settings = world.ws.sccp_general_settings.view()
    yield settings
    dict_obj = settings.to_obj_dict()
    world.ws.sccp_general_settings.raw_edit(None, dict_obj)

def disable_directmedia():
    with sccp_settings() as settings:
        settings.directmedia = False

def enable_directmedia():
    with sccp_settings() as settings:
        settings.directmedia = True

def set_dialtimeout(timeout):
    with sccp_settings() as settings:
        settings.dialtimeout = timeout

def set_language(language):
    with sccp_settings() as settings:
        settings.language = language


