from site import getsitepackages
from watchdog.observers import Observer
from .handler import PackageUpdatesHandler


def reset_on_package_updates(app):
    handler = PackageUpdatesHandler(app)
    observer = Observer()
    observer.schedule(handler, getsitepackages()[0], recursive=False)
    observer.start()
