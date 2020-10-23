import sys

from ...commands import BasicCommand
from . import ConfigValue, NOT_SET, LOCATION


class ConfigureListCommand(BasicCommand):
    NAME = 'list'
    DESCRIPTION = (
        'List the MNG CLI configuration data. This command will '
        'show you the current configuration data. For each configuration '
        'item, it will show you the value, where the configuration value '
        'was retrieved, and the configuration variable name. For example, '
        'if you provide the AWS region in an environment variable.\n'
    )
    SYNOPSIS = 'mng configure list'
    EXAMPLES = (
        'To show your current configuration values::\n'
        '\n'
        '  $ mng configure list\n'
        '        Name                    Value             Type    Location\n'
        '        ----                    -----             ----    --------\n'
        '      ip_api               10.0.0.100              str    ~/.mng/config\n'
        '    port_api                     8080              int    ~/.mng/config\n'
        '    user_api                      api              str    ~/.mng/config\n'
        '  passwd_api     ****************ABCD              str    ~/.mng/config\n'
        '  base64auth     ****************ABCD              str    ~/.mng/config\n'
        '\n'
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

        user_api = self._lookup_config('user_api')
        self._display_config_value(user_api, 'user_api')

        passwd_api = self._lookup_credentials()
        self._display_config_value(passwd_api, 'passwd_api')

    
    def _display_config_value(self, config_value, config_name):
        config_value = config_value[0] if isinstance(config_value, tuple) else config_value
        self._stream.write('%10s %24s %16s    %s\n' % (
            config_name, config_value.value, config_value.config_type,
            config_value.config_variable))

    def _lookup_credentials(self):
        # First try it with _lookup_config.  It's possible
        # that we don't find credentials this way (for example,
        # if we're using an IAM role).
        passwd_api = self._lookup_config('passwd_api')
        if passwd_api.value is not NOT_SET:
            passwd_api.mask_value()
            return passwd_api
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
                passwd_api = ConfigValue(credentials.passwd_api,
                                         credentials.method, '')
                passwd_api.mask_value()
                return passwd_api

    def _lookup_config(self, name):
        # Then try to look up the variable in the config file.
        value = None
        if value is not None:
            return ConfigValue(value, 'config-file', LOCATION)
        else:
            return ConfigValue(NOT_SET, None, None)
