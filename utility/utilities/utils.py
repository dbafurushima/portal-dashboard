import os
import time
import pickle
from .utils_constants import (DEFAULT_DEBUG_LOG, DEFAULT_ENABLED_DEBUG, DEFAULT_ENABLED_LOG)


def debug(
        text: str,
        is_enabled_log: bool = DEFAULT_ENABLED_LOG,
        is_enabled_debug: bool = DEFAULT_ENABLED_DEBUG) -> None:

    timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime(time.time()))

    if is_enabled_log:
        with open(DEFAULT_DEBUG_LOG, mode='a+', encoding='utf-8') as fp:
            fp.write('%s %s\n' % (timestamp, text))

    if is_enabled_debug:
        print('%s %s' % (timestamp, text))


def error_to_user(msg):
    print('\n>> Ops... error, %s\n' % msg)


def save_working_status(worker, path):
    pickle.dump(worker, open(path, 'wb'))