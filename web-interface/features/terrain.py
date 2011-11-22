# -*- coding: UTF-8 -*-

from lettuce import before, after, world
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from xivobrowser import XiVOBrowser

def _wait_for_id(elementId, message='', timeout=5):
    try:
        WebDriverWait(world.browser, timeout).until(lambda browser : browser.find_element_by_id(elementId))
    except TimeoutException:
        raise Exception(elementId, message)
    finally:
        pass

def _wait_for_name(elementId, message='', timeout=5):
    try:
        WebDriverWait(world.browser, timeout).until(lambda browser : browser.find_element_by_name(elementId))
    except TimeoutException:
        raise Exception(elementId, message)
    finally:
        pass

@before.all
def setup_browser():
    from pyvirtualdisplay import Display
    Display(visible=0, size=(1024, 768)).start()
    world.browser = XiVOBrowser()
    world.wait_for_id = _wait_for_id
    world.wait_for_name = _wait_for_name

# Use this if you want to debug your test
# Call it with world.dump_current_page()
@world.absorb
def dump_current_page(filename='/tmp/lettuce.html'):
    world.wait_for_id('version-copyright', 'Page not loaded')
    f = open(filename, 'w')
    f.write(world.browser.page_source.encode('utf-8'))
    f.close()

@after.all
def teardown_browser(total):
    world.browser.quit()
