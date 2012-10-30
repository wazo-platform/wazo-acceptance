# -*- coding: utf-8 -*-

from lettuce import step
from xivo_lettuce.manager import file_manager


@step(u'Given a recording file with name "([^"]*)"')
def given_a_recording_file_with_name(step, filename):
    file_manager.create_recordings_file(filename)


@step(u'Given a recording meetme file with name "([^"]*)"')
def given_a_recording_meetme_file_with_name(step, filename):
    file_manager.create_recordings_meetme_file(filename)


@step(u'Given a musiconhold file with name "([^"]*)"')
def given_a_musiconhold_file_with_name(step, filename):
    file_manager.create_musiconhold_file(filename)
