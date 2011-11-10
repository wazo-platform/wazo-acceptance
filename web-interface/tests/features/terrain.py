from lettuce import before, after, world
from selenium import webdriver


@before.all
def setup_browser():
    from pyvirtualdisplay import Display
    Display(visible=0, size=(1024, 768)).start()
    world.browser = webdriver.Firefox()

@after.all
def teardown_browser(total):
    pass
    #world.browser.quit()
