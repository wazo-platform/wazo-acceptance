# -*- coding: utf-8 -*-

import json
import time
from lettuce.registry import world
from xivo_lettuce.common import open_url, get_value_with_label

def rest_api_configuration():
    open_url('provd_general')
    host = get_value_with_label("API REST IP")
    port = get_value_with_label("API REST port")
    return host, int(port)


def rest_put(host, port, uri, value):
    data = {'param': {'value': value}}
    url = "http://%s:%s%s" % (host, port, uri)

    command = [
        'curl'        ,
        '--write-out' , "'%{http_code}'"                                           ,
        '-X'          , 'PUT'                                                      ,
        '-H'          , "'Content-Type: application/vnd.proformatique.provd+json'" ,
        '-d'          , "'%s'" % json.dumps(data)                                  ,
        url
    ]

    output = world.ssh_client_xivo.out_call(command)
    if int(output) >= 400:
        raise Exception("could not update provd through rest API")


def configure_proxies(config):
    fields = {
        'http_proxy': 'http proxy',
        'ftp_proxy': 'ftp proxy',
        'https_proxy': 'https proxy',
    }

    for input_name, config_name in fields.items():
        element = world.browser.find_element_by_name(input_name)
        element.clear()
        element.send_keys(config.get(config_name, ''))
        time.sleep(3)


def type_plugin_server_url(url):
    world.browser.find_element_by_name('plugin_server', 'plugin_server form not loaded')
    input_plugin_server = world.browser.find_element_by_name('plugin_server')
    input_plugin_server.clear()
    input_plugin_server.send_keys(url)
    time.sleep(2)


def update_plugin_server_url(url):
    open_url('provd_general')
    type_plugin_server_url(url)
