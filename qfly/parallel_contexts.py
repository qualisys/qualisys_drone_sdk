# Based on: https://code.activestate.com/recipes/577352-starting-several-context-managers-concurrently/

from __future__ import with_statement

import sys
import threading
import traceback


__all__ = ["MultipleError", "parallel"]


class ParallelContexts(object):

    """Concurrently start and stop serveral context managers in different
    threads.

    Typical usage::

        with parallel(Foo(), Bar()) as managers:
            foo, bar = managers
            foo.do_something()
            bar.do_something()

    """

    def __init__(self, *managers):
        self.managers = managers

    def __enter__(self):
        errors = []
        threads = []

        for mgr in self.managers:
            t = threading.Thread(target=run,
                                 args=(mgr.__enter__, tuple(), errors))
            t.start()
            threads.append(t)
        for thread in threads:
            thread.join()

        if errors:
            err = MultipleError(errors)
            raise err

        return self.managers

    def __exit__(self, *exc_info):
        errors = []
        threads = []

        for mgr in self.managers:
            t = threading.Thread(target=run,
                                 args=(mgr.__exit__, exc_info, errors))
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()

        if errors:
            raise MultipleError(errors)


class MultipleError(Exception):

    """Exception class to collect several errors in a single object."""

    def __init__(self, errors):
        super(Exception, self).__init__()
        self.errors = errors

    def __str__(self):
        bits = []
        for exc_type, exc_val, exc_tb in self.errors:
            bits.extend(traceback.format_exception(exc_type, exc_val, exc_tb))
        return "".join(bits)


def run(func, args, errors):
    """Helper for ``parallel``.

    """
    try:
        func(*args)
    except:
        errors.append(sys.exc_info())