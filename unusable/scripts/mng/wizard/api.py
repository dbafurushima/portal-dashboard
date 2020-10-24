# ==============================================================================
# IMPORTS
# ==============================================================================
import os
import json
import getpass
import base64
from datetime import datetime
from mng.helper.cli import (
    Answer,
    choose,
    confirm,
    readline,
)
from mng.helper.log import app_log
from mng.model.base import ToolConfiguration
# ==============================================================================
# CLASSES
# ==============================================================================
class ApiConfigurationWizard:
    """[summary]
    """
    def __init__(self, prev_conf=None):
        """[summary]
        """
        # params
        if not prev_conf:
            prev_conf = {}
        self.default = {
            'ip': prev_conf.get('ip', 'localhost'),
            'port': prev_conf.get('port', 8080),
            'user': prev_conf.get('user', 'api'),
            'passwd': prev_conf.get('passwd'),
            'base64auth': prev_conf.get('base64auth')
        }
        self._ip = self.default['ip']
        self._port = self.default['port']
        self._user = self.default['user']
        self._passwd = self.default['passwd']
        self._base64auth = self.default['base64auth']

    @property
    def result(self):
        return ToolConfiguration({
            'api': {
                'ip': self._ip,
                'port': self._port,
                'credentials': {
                    'user': self._user,
                    'passwd': self._passwd,
                    'base64auth': self._base64auth
                }
        }})

    def show(self):
        while True:
            self._ip = readline("endereço IP da API", default=self.default['ip'])
            self._port = int(readline("porta em que a API está executando", default=self.default['port']))
            self._user = readline("usuário para acesso", default=self.default['user'])
            self._passwd = getpass.getpass(prompt='senha para acesso: ', stream=None)
            base64auth = '%s:%s' % (self._user, self._passwd)
            self._base64auth = base64.b64encode(base64auth.encode("utf-8")).decode('utf-8')#.replace('\n', '')
            # confirm, abort or retry
            answer = confirm(f"Are you ok with this configuration:\n{json.dumps(self.result, indent=4)}", abort=True)
            if answer == Answer.YES:
                return True
            elif answer == Answer.ABORT:
                app_log.warning("user canceled the operation.")
                return False
