from ruamel.yaml import YAML
from mng.helper.exception import SaTException
from mng.helper.log import app_log


class MetaConfiguration(type):
    ABSTRACT_CLASSES = {'Configuration'}
    EXPECTED_MEMBERS = {'TYPE', 'DEFINITION'}

    def __new__(cls, name, bases, dct):
        ncls = super().__new__(cls, name, bases, dct)
        if name in MetaConfiguration.ABSTRACT_CLASSES:
            return ncls
        for member in MetaConfiguration.EXPECTED_MEMBERS:
            if not dct.get(member):
                raise AttributeError(f"missing '{member}' in MetaConfiguration subclass!")
        return ncls

# pylint: disable=E1101


class Configuration(dict, metaclass=MetaConfiguration):
    """classe template para validar arquivos de configuração apartir de um modelo ``DEFINITION``
    - carrega objeto apartir de um arquivo .yml
    - valida se está no formato correto
    """

    @classmethod
    def load(cls, path):
        """load and build a class from a YAML configuration
        """
        conf = cls()
        if path.is_file():
            try:
                app_log.debug(f"loading {cls.TYPE} configuration from {path}")
                conf = YAML(typ='safe').load(path)
                conf = cls(conf)
            except:
                app_log.critical(f"failed to load {cls.TYPE} configuration from {path}")
                raise SaTException("configuration load failed.")
        return conf

    @property
    def raw(self):
        return dict(self)

    def __dict_check(self, obj, expected_obj, chain='') -> bool:
        """Recursive diffing and type checking between two dicts
        """
        if isinstance(expected_obj, dict) and isinstance(obj, dict):
            for ek, ev in expected_obj.items():
                v = obj.get(ek)
                chain += f'.{ek}'
                if v is None:
                    app_log.warning(f"invalid {self.TYPE} configuration - missing key: {chain}")
                    return False
                if not self.__dict_check(v, ev, chain):
                    return False
        elif isinstance(expected_obj, tuple):
            if not isinstance(obj, expected_obj):
                app_log.warning(f"invalid {self.TYPE} configuration - {chain} has invalid type: {obj} ({type(obj)})")
                return False
        else:
            app_log.warning(f"invalid {self.TYPE} configuration - {chain} should be a dict: {obj}")
            return False
        return True

    def validate(self, throw=True) -> bool:
        """Determine if self is valid against expected_obj definition
        """
        if not self.__dict_check(self, self.DEFINITION):
            if throw:
                raise SaTException(f"{self.TYPE} configuration is missing or invalid.")
            else:
                return False
        return True

    def save(self, path) -> None:
        """Serialize self to a file using YAML format
        """
        yaml = YAML(typ='safe')
        yaml.default_flow_style = False
        with path.open('w+') as fp:
            fp.write("#\n"
                     "# This file was generated using MNG utility.\n"
                     "# Do not edit it manually unless you know exactly what you're doing.\n"
                     "#\n")
            yaml.dump(self.raw, fp)
