import atexit
import contextlib
import importlib.resources as resources


# A single ExitStack holds every resource extracted during the process lifetime.
# Registering its close() once with atexit (rather than once per call) avoids
# the unbounded growth of atexit handlers that the old implementation caused.
_file_manager = contextlib.ExitStack()
atexit.register(_file_manager.close)


def resource_filename(package, resource):
    """Return a filesystem path for a resource bundled inside a package.

    Uses importlib.resources.files(...).joinpath(...) + as_file(), which is the
    modern replacement for the deprecated importlib.resources.path().  When the
    package is installed from a zip/wheel, as_file() materializes a temporary
    copy on disk and cleans it up at interpreter exit.
    """
    ref = resources.files(package).joinpath(resource)
    return str(_file_manager.enter_context(resources.as_file(ref)))
