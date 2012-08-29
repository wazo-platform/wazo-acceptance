# -*- coding: utf-8 -*-

from lettuce.registry import world


def exten_line(exten):
    """Find the line of an outcall exten in the list of an outcall extens."""
    return world.browser.find_element_by_xpath(
        "//table[@id='list_exten']//tr[.//input[@name='dialpattern[exten][]' and @value='%s']]" % exten)
