import sys
import os
import time
import multiprocessing
from watchdog.events import FileSystemEventHandler


def restart_server():
    print('Restarting in 5 seconds')
    time.sleep(3)
    print('Restarting the server')
    PackageUpdatesHandler.app.terminate()
    os.execv(sys.argv[0], sys.argv)


class PackageUpdatesHandler(FileSystemEventHandler):
    scheduled = None
    app = None


    def __init__(self, app):
        PackageUpdatesHandler.app = app


    @staticmethod
    def schedule_reset():
        if PackageUpdatesHandler.scheduled:
            PackageUpdatesHandler.scheduled.terminate()
        PackageUpdatesHandler.scheduled = multiprocessing.Process(target=restart_server)
        PackageUpdatesHandler.scheduled.start()


    @staticmethod
    def on_created(event):
        print(f'created! {event.src_path}')
        PackageUpdatesHandler.schedule_reset()


    @staticmethod
    def on_deleted(event):
        print(f'Deleted! {event.src_path}')
        PackageUpdatesHandler.schedule_reset()
