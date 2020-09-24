import shutil
from pathlib import Path
from mng.helper.fs import scandir
from mng.helper.log import app_log
from mng.wizard.api import ApiConfigurationWizard
from .base import ToolConfiguration
import logging
import pathlib


class ApiConfig:
    """classe para armazenar, configurar e salvar arquivo e configuração 
    com credenciais de acesso a API
    """
    def __init__(self, conf=None):
        self._conf = conf
        self._conf_path = ToolConfiguration.LOCATION
        if not conf:
            self._conf = ToolConfiguration.load(self._conf_path)
            if not self._conf.validate(throw=False):
                app_log.warning("api config requires initialization.")

    @property
    def conf(self):
        return self._conf

    @property
    def path(self):
        return self._conf_path.parent

    @property
    def initialized(self):
        return self._conf_path.is_file()

    def _save_conf(self):
        """save configuration credentials to disk
        """
        if not self._conf.validate(throw=False):
            app_log.error("save operation aborted: invalid configuration")
            return False
        self._conf.save(self._conf_path)
        return True

    def init(self):
        """[summary]
        """
        if not self.initialized:
            wizard = ApiConfigurationWizard(self._conf)
            if not wizard.show():
                return False
            self._conf = wizard.result
            self.path.mkdir(parents=True, exist_ok=True)
            # app_log.info("copying configurations...")
            # shutil.copytree(str(GeneralConfiguration.LOCATION), str(self.monitoring_dir))
            app_log.info("saving repository configuration...")
            return self._save_conf()
        return False

    def scan(self, tags=[], categories=[]):
        """Returns a list of challenges having at least one tag in common with tags
        An empty list of tags means all tags
        """
        pass

    def find(self, slug):
        """Finds challenge
        """
        pass

    def configure(self, override_conf=None):
        """Configures general infos
        """
        final_conf = override_conf
        if not final_conf:
            wizard = ApiConfigurationWizard(self.conf)
            if not wizard.show():
                return False
            final_conf = wizard.result
        self._conf = final_conf
        return self._save_conf()
