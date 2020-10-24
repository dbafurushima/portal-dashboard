from pathlib import Path
from mng.helper.exception import MNGException
from .configuration import Configuration


class ToolConfiguration(Configuration):
    """[summary]
    """
    TYPE = 'api'
    DEFINITION = {
        'api': {
            'ip': (str,),
            'port': (int,), 
            'credentials': {
                'user': (str,),
                'passwd': (str,),
                'base64auth': (str,)
            }
        }
    }

    LOCATION = Path.home().joinpath('.config', 'mng', 'mng.yml')

    @classmethod
    def load(cls, path):
        if not path:
            path = ToolConfiguration.LOCATION
        return super(ToolConfiguration, cls).load(path)

    @property
    def ip(self) -> str:
        return self['api']['ip']
    
    @property
    def port(self) -> int:
        return self['api']['port']

    @property
    def user(self) -> str:
        return self['api']['credentials']['user']

    @property
    def passwd(self) -> str:
        return self['api']['credentials']['passwd']
    
    @property
    def base64auth(self) -> str:
        return self['api']['credentials']['base64auth']
