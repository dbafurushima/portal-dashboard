import psutil
import pickle
from typing import List, Tuple
from .utils import debug, save_working_status
from .utils_constants import DEFAULT_WORKER_PATH


def _status_process(ps: psutil.Process):
    return ps.status


class Process(object):

    def __init__(self,
            pid: int,
            ps: psutil.Process or None,
            params: dict) -> None:

        self.pid = pid
        self.ps = ps
        self.params = params


class Worker:

    def __init__(self):
        self.running: List[Process] = []
        self.stopped: List[Process] = []

    def put(self, pid: int, params: dict) -> None:
        debug('add new process with pid %s and with parameters "%s"' % (pid, params))

        try:
            ps = psutil.Process(pid=pid)
            self.running.append(
                Process(pid, ps, params))
        except (PermissionError, psutil.AccessDenied):
            self.running.append(
                Process(pid, None, params))
        self._update_status_process()

    def get(self, pid: int) -> Process:
        for task in self.running + self.stopped:
            if task.pid == pid:
                return Process
        return None

    def update(self, pid: int) -> None:
        debug('updating process status with pid "%s" to stopped' % pid)

        index_pid = None
        for index, task in enumerate(self.running):
            if task.pid == pid:
                index_pid = index
                break
        if index_pid is not None:
            if not self.running[index_pid] in self.stopped:
                self.stopped.append(self.running[index_pid])
            self.running.pop(index_pid)
        self._update_status_process()

    def status(self, pid: int) -> bool or None:
        for task in self.running:
            if task.pid == pid:
                return _status_process(task.ps)
        return None

    def status_all(self):
        return self.running + self.stopped

    def kill(self, task):
        pass

    def killall(self):
        pass

    def _update_status_process(self):
        # save_working_status(self, DEFAULT_WORKER_PATH)
        pass

    def __str__(self):
        output = 'RUNNING:\n'
        for index, task in enumerate(self.running):
            output += 'task - [%s] [name: %s] [pid: %s]\n' % (index, task.name(), task.pid)
        output += 'STOPPED:\n'
        for index, task in enumerate(self.stopped):
            output += 'task - [%s] [name: %s] [pid: %s]\n' % (index, task.name(), task.pid)
        return output