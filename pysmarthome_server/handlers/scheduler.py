import sys
import os
import time
import signal
from multiprocessing import Process


class Scheduler:
    _scheduled = None


    @staticmethod
    def restart(pid):
        print('Restarting in 3 seconds')
        time.sleep(3)
        print('Restarting the server')
        os.kill(pid, signal.SIGTERM)
        os.execv(sys.argv[0], sys.argv)


    @staticmethod
    def unschedule():
        if Scheduler._scheduled:
            Scheduler._scheduled.terminate()


    @staticmethod
    def schedule_restart(**args):
        if not args: return
        Scheduler.unschedule()
        _scheduled = Process(target=Scheduler.restart, args=(os.getpid(),))
        _scheduled.start()
