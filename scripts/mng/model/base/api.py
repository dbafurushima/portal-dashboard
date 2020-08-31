from pathlib import Path
from mng.helper.exception import SaTException
from .configuration import Configuration


class ApiConfiguration(Configuration):
    """[summary]
    """
    TYPE = 'api'
    DEFINITION = {
        'host': {
            'ip': (str,),
            'port': (int,), 
            'credentials': {
                'user': (str,),
                'passwd': (str,)
            }
        }
    }

    LOCATION = Path.home().joinpath('.config', 'mng', 'mng.yml')

    @classmethod
    def load(cls, path):
        if not path:
            path = ApiConfiguration.LOCATION
        return super(ApiConfiguration, cls).load(path)

    @property
    def ip(self) -> str:
        return self['host']['ip']
    
    @property
    def port(self) -> int:
        return self['host']['port']

    @property
    def user(self) -> str:
        return self['host']['credentials']['user']

    @property
    def passwd(self) -> str:
        return self['host']['credentials']['passwd']
