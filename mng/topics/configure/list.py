import sys
import configparser

from ...commands import BasicCommand
from . import ConfigValue, NOT_SET, LOCATION


class ConfigureListCommand(BasicCommand):
    NAME = 'list'
    DESCRIPTION = (
        'Liste os dados de configuração MNG CLI. Este comando mostrará '
        'os dados de configuração atuais. Para cada item de configuração, '
        'ele mostrará o valor, onde o valor de configuração foi recuperado '
        'e o nome da variável de configuração.'
    )
    SYNOPSIS = 'mng configure list'
    EXAMPLES = (
        '\nPara mostrar seus valores de configuração atuais\n'
        '\n'
        '  $ mng configure list\n'
        '        Name                    Value             Type    Location\n'
        '        ----                    -----             ----    --------\n'
        ' address_api               10.0.0.100              str    ~/.config/mng.ini\n'
        '    port_api                     8080              int    ~/.config/mng.ini\n'
        'username_api                      api              str    ~/.config/mng.ini\n'
        'password_api     ****************ABCD              str    ~/.config/mng.ini\n'
        '  base64auth     ****************ABCD              str    ~/.config/mng.ini'
    )

    def __init__(self, stream=sys.stdout):
        super(ConfigureListCommand, self).__init__()
        self._stream = stream

    def _run_main(self, args, parsed_globals):
        print('ConfigureListCommand._run_main()')
        self._display_config_value(ConfigValue('Value', 'Type', 'Location'),
                                   'Name')
        self._display_config_value(ConfigValue('-----', '----', '--------'),
                                   '----')

        address_api = self._lookup_config('address_api')
        self._display_config_value(address_api, 'address_api')

        port_api = self._lookup_config('port_api')
        self._display_config_value(port_api, 'port_api')

        username_api = self._lookup_config('username_api')
        self._display_config_value(username_api, 'username_api')

        password_api, base64auth = self._lookup_credentials()
        self._display_config_value(password_api, 'password_api')
        self._display_config_value(base64auth, 'base64auth')

    
    def _display_config_value(self, config_value, config_name):
        config_value = config_value[0] if isinstance(config_value, tuple) else config_value
        self._stream.write('%15s %30s %20s    %s\n' % (
            config_name, config_value.value, config_value.config_type,
            config_value.config_variable))

    def _lookup_credentials(self):
        # First try it with _lookup_config.  It's possible
        # that we don't find credentials this way (for example,
        # if we're using an IAM role).
        password_api = self._lookup_config('password_api')
        if password_api.value is not NOT_SET:
            password_api.mask_value()
            base64auth = self._lookup_config('base64auth')
            base64auth.mask_value()
            return password_api, base64auth
        else:
            # Otherwise we can try to use get_credentials().
            # This includes a few more lookup locations
            # (IAM roles, some of the legacy configs, etc.)
            credentials = None
            if credentials is None:
                no_config = ConfigValue(NOT_SET, None, None)
                return no_config, no_config
            else:
                # For the ConfigValue, we don't track down the
                # config_variable because that info is not
                # visible from botocore.credentials.  I think
                # the credentials.method is sufficient to show
                # where the credentials are coming from.
                password_api = ConfigValue(credentials.password_api,
                                         credentials.method, '')
                password_api.mask_value()
                base64auth = ConfigValue(credentials.base64auth,
                                         credentials.method, '')
                base64auth.mask_value()
                return password_api, base64auth

    def _lookup_config(self, name):
        # Then try to look up the variable in the config file.
        configp = configparser.ConfigParser()
        configp.read(LOCATION)
        value = configp['default'][name]
        if value is not None:
            return ConfigValue(value, 'config-file', LOCATION)
        else:
            return ConfigValue(NOT_SET, None, None)
