# -*- coding: utf-8 -*-
import time

from lettuce import before, after, world

from xivobrowser import XiVOBrowser

@before.all
def setup_browser():
    from pyvirtualdisplay import Display
    Display(visible=0, size=(1024, 768)).start()
    world.browser = XiVOBrowser()
    world.timeout = 5

@before.all
def setup_login_infos():
    world.login = 'root'
    world.password = 'superpass'
    world.host = 'http://skaro-daily.lan-quebec.avencall.com/'

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
