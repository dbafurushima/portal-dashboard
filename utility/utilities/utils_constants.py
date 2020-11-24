import os

DEFAULT_BACKUP = False
DEFAULT_THROW = False
DEFAULT_TURN = 5
DEFAULT_CLI_ENABLE_BACKUP = False
DEFAULT_ENABLED_DEBUG = True
DEFAULT_ENABLED_LOG = True

CHOICES_PER_TIME = {
    'week': 604800, 'day': 86400, 'hour': 3600, 'minute': 60, 'second': 1
}
CHOICES_PRIORITY = [1, 2]

CHOICES_TYPE_RESOURCE = ['cpu', 'mem']

DEFAULT_WORKER_PATH = os.getenv('DEFAULT_WORKER_PATH', '/tmp/cli_WORKER.ps')
DEFAULT_DEBUG_LOG = '/tmp/debug_mode.log'