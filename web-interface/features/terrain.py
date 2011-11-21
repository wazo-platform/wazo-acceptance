from lettuce import before, after, world
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from xivobrowser import XiVOBrowser

def _waitFor(elementId, message='', timeout=5):
    try:
        WebDriverWait(world.browser, timeout).until(lambda browser : browser.find_element_by_id(elementId))
    except TimeoutException:
        raise Exception(elementId, message)
    finally:
        pass

@before.all
def setup_browser():
    from pyvirtualdisplay import Display
    Display(visible=0, size=(1024, 768)).start()
    world.browser = XiVOBrowser()
    world.waitFor = _waitFor

@world.absorb
def dump_current_page(filename='/tmp/lettuce.html'):
    world.waitFor('version-copyright', 'Page not loaded')
    f = open(filename, 'w')
    f.write(world.browser.page_source.encode('utf-8'))
    f.close()

@after.all
def teardown_browser(total):
    world.browser.quit()
