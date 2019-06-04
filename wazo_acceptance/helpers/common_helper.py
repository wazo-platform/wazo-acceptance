# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import time


class NoMoreTries(Exception):
    pass


class CommonHelper:

    def wait_until(self, function, *args, **kwargs):
        """Run <function> <tries> times, spaced with 1 second. Stops when <function>
        returns an object evaluating to True, and returns it.

        Useful for waiting for an event.

        Arguments:

            - function: the function detecting the event
            - message: the message raised if <function> does not return something
              after <tries> times
            - tries: the number of times to run <function>
        """

        message = kwargs.pop('message', None)
        tries = kwargs.pop('tries', 1)
        return_value = False

        for _ in range(tries):
            return_value = function(*args, **kwargs)
            if return_value:
                return return_value
            time.sleep(1)
        else:
            raise NoMoreTries(message)
