from lettuce import before, after, world
from selenium import webdriver


@before.all
def setup_browser():
    world.browser = webdriver.Firefox()

@after.all
def teardown_browser(total):
    world.browser.quit()
