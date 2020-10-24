import os

from ...commands import BasicCommand
from .writer import ConfigFileWriter

from . import PREDEFINED_SECTION_NAMES, profile_to_section, LOCATION


class ConfigureSetCommand(BasicCommand):
    NAME = 'set'
    DESCRIPTION = BasicCommand.FROM_FILE('configure', 'set',
                                         '_description.rst')
    SYNOPSIS = 'aws configure set varname value [--profile profile-name]'
    EXAMPLES = BasicCommand.FROM_FILE('configure', 'set', '_examples.rst')
    ARG_TABLE = [
        {'name': 'varname',
         'help_text': 'The name of the config value to set.',
         'action': 'store',
         'cli_type_name': 'string', 'positional_arg': True},
        {'name': 'value',
         'help_text': 'The value to set.',
         'action': 'store',
         'no_paramfile': True,  # To disable the default paramfile behavior
         'cli_type_name': 'string', 'positional_arg': True},
    ]
    # Any variables specified in this list will be written to
    # the ~/.aws/credentials file instead of ~/.aws/config.
    _WRITE_TO_CREDS_FILE = ['address_api', 'username_api',
                            'port_api', 'password_api']

    def __init__(self, config_writer=None):
        super(ConfigureSetCommand, self).__init__()
        if config_writer is None:
            config_writer = ConfigFileWriter()
        self._config_writer = config_writer

    def _run_main(self, args, parsed_globals):
        varname = args.varname
        value = args.value
        section = 'default'
        config_filename = LOCATION
        # Before handing things off to the config writer,
        # we need to find out three things:
        # 1. What section we're writing to (section).
        # 2. The name of the config key (varname)
        # 3. The actual value (value).
        if '.' not in varname:
            pass
        else:
            # First figure out if it's been scoped to a profile.
            parts = varname.split('.')
            if parts[0] in ('default', 'profile'):
                # Then we know we're scoped to a profile.
                if parts[0] == 'default':
                    section = 'default'
                    remaining = parts[1:]
                else:
                    # [profile, profile_name, ...]
                    section = profile_to_section(parts[1])
                    remaining = parts[2:]
                varname = remaining[0]
                if len(remaining) == 2:
                    value = {remaining[1]: value}
            elif len(parts) == 2:
                # Otherwise it's something like "set preview.service true"
                # of something in the [plugin] section.
                section, varname = parts
        updated_config = {'__section__': section, varname: value}
        if varname in self._WRITE_TO_CREDS_FILE:
            section_name = updated_config['__section__']
            if section_name.startswith('profile '):
                updated_config['__section__'] = section_name[8:]
        self._config_writer.update_config(updated_config, config_filename)
