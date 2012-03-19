# -*- coding: UTF-8 -*-

import subprocess


class ScreenParsingException(Exception):
    pass


def get_session_names():
    screen_output = _get_list_output()
    return _parse_list_output(screen_output)


def _get_list_output():
    return _get_command_output(['screen', '-list'])


def _get_command_output(args):
    process = subprocess.Popen(args, stdout=subprocess.PIPE)
    return process.communicate()[0]


def _parse_list_output(screen_output):
    # Current limitation: does not parse correctly session name
    # with space in it
    if screen_output.startswith('No Sockets found'):
        return []
    else:
        session_names = []
        lines = screen_output.split('\n')
        for screen_line in lines[1:]:
            if not screen_line.startswith('\t'):
                break
            session_names.append(_parse_list_line(screen_line))
        if not session_names:
            raise ScreenParsingException()
        return session_names


def _parse_list_line(screen_line):
    first_token = screen_line.lstrip().split(None, 1)[0]
    session_name = first_token.split('.', 1)[1]
    if not session_name:
        raise ScreenParsingException()
    return session_name
