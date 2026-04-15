import atexit
import contextlib

import importlib.resources


def resource_filename(package, resource):
    """Create a filename resource from a package and its resource."""
    file_manager = contextlib.ExitStack()
    atexit.register(file_manager.close)

    return str(file_manager.enter_context(importlib.resources.path(package, resource)))
