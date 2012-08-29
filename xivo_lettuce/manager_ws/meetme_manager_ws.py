# -*- coding: utf-8 -*-

from xivo_lettuce.common import get_webservices

WS = get_webservices('meetme')


def delete_meetme_with_confno(confno):
    for id in find_meetme_id_with_confno(confno):
        WS.delete(id)


def find_meetme_id_with_confno(confno):
    list = WS.search(confno)
    if list:
        return [meetme['id'] for meetme in list if
                meetme['confno'] == confno]
    return []
