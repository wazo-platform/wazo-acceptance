# -*- coding: utf-8 -*-

from lettuce import world


def webi_exec_commonconf():
    url = '%s%s' % (world.host, '/xivo/configuration/index.php/controlsystem/commonconf')
    world.browser.get(url)
