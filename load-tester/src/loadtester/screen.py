# -*- coding: UTF-8 -*-

import subprocess


class ScreenParsingException(Exception):
    pass


def _parse_list_line(screen_line):
    first_token = screen_line.lstrip().split(None, 1)[0]
    session = first_token.split(".", 1)[1]
    if not session:
        raise ScreenParsingException()
    return session


def parse_list_output(screen_output):
    # Current limitation: does not parse correctly session name
    # with space in it
    if screen_output.startswith("No Sockets found"):
        return []
    else:
        sessions = []
        lines = screen_output.split("\n")
        for screen_line in lines[1:]:
            if not screen_line.startswith("\t"):
                break
            sessions.append(_parse_list_line(screen_line))
        if not sessions:
            raise ScreenParsingException()
        return sessions


def _get_command_output(args):
    process = subprocess.Popen(args, stdout=subprocess.PIPE)
    return process.communicate()[0]


def get_list_output():
    return _get_command_output(["screen", "-list"])


def get_sessions():
    screen_output = get_list_output()
    return parse_list_output(screen_output)
