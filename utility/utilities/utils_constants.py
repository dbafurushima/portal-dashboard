import os
import sys
import base64

DEFAULT_MESSAGE_SET_ENVVARS = ('\nYou must set the API access credentials in the environment variables.\n'
                               'Use the following commands for the linux environment:\n\n'
                               'export API_USER="your-api-username"\n'
                               'export API_PASSWD="your-api-password"\n')

DEFAULT_BACKUP = False
DEFAULT_THROW = False
DEFAULT_TURN = 5
DEFAULT_CLI_ENABLE_BACKUP = False
DEFAULT_ENABLED_DEBUG = False
DEFAULT_ENABLED_LOG = True

CHOICES_PER_TIME = {
    'week': 604800, 'day': 86400, 'hour': 3600, 'minute': 60, 'second': 1
}
CHOICES_PRIORITY = [1, 2]

CHOICES_TYPE_RESOURCE = ['cpu', 'mem']

DEFAULT_WORKER_PATH = os.getenv('DEFAULT_WORKER_PATH', '/tmp/cli_WORKER.ps')
DEFAULT_DEBUG_LOG = '/tmp/debug_mode.log'

DEFAULT_API_USER = os.getenv('API_USER', 'None')
DEFAULT_API_PASSWD = os.getenv('API_PASSWD', 'None')

DEFAULT_URL_BASE_API = os.getenv('API_URL' ,'http://192.168.1.3:8000')
DEFAULT_HEADERS = {'Authorization': 'Basic %s' % base64.b64encode(
    (DEFAULT_API_USER + ':' + DEFAULT_API_PASSWD).encode("utf-8")).decode('utf-8')}