import os
import pickle
import datetime
from .worker import Worker
from .utils import debug
from .utils_constants import DEFAULT_WORKER_PATH

WORKER = Worker()

if os.path.exists(DEFAULT_WORKER_PATH):
    with open(DEFAULT_WORKER_PATH, 'rb') as in_s:
        while True:
            try:
                o = pickle.load(in_s)
            except EOFError:
                break
            else:
                WORKER = o
                debug('load WORKER from %s' % DEFAULT_WORKER_PATH)
else:
    try:
        with open(DEFAULT_WORKER_PATH, 'wb') as in_s:
            pickle.dump(WORKER, in_s)
        debug('new WORKER from %s' % DEFAULT_WORKER_PATH)
    except PermissionError:
        now = datetime.datetime.now()
        new_tempfile = '/tmp/%s_WORKER.ps' % now.strftime('%m-%d_%H-%M-%S')

        with open(new_tempfile, 'wb') as in_s:
            pickle.dump(WORKER, in_s)

        os.environ["DEFAULT_WORKER_PATH"] = new_tempfile
        DEFAULT_WORKER_PATH = new_tempfile
        debug('new WORKER from tempfile %s' % new_tempfile)