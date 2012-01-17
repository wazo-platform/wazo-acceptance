# -*- coding: utf-8 -*-

from lettuce import before, after, world
from xivobrowser import XiVOBrowser

@before.all
def setup_browser():
    from pyvirtualdisplay import Display
    # Display(visible=0, size=(1024, 768)).start()
    world.browser = XiVOBrowser()
    world.timeout = 1


@before.all
def setup_login_infos():
    world.login = 'test'
    world.password = 'superpass'
    world.host = 'http://192.168.0.182/'
    # world.login = 'root'
    # world.password = 'superpass'
    # world.host = 'http://skaro-daily.lan-quebec.avencall.com/'

@world.absorb
def dump_current_page(filename='/tmp/lettuce.html'):
    """Use this if you want to debug your test
       Call it with world.dump_current_page()"""
    f = open(filename, 'w')
    f.write(world.browser.page_source.encode('utf-8'))
    f.close()
    world.browser.save_screenshot(filename + '.png')


@after.all
def teardown_browser(total):
    world.browser.quit()
