from lettuce import before, after, world
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

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
    world.browser = webdriver.Firefox()
    world.waitFor = _waitFor

@after.all
def teardown_browser(total):
    pass
    world.browser.quit()
