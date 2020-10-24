import os
import base64

from ...commands import BasicCommand
from .list import ConfigureListCommand
from .set import ConfigureSetCommand
from .writer import ConfigFileWriter
from . import LOCATION, mask_value, profile_to_section


class InteractivePrompter(object):

    def get_value(self, current_value, config_name, prompt_text=''):
        if config_name in ('base64auth', 'passwd_api'):
            current_value = mask_value(current_value)
        response = input("%s [%s]: " % (prompt_text, current_value))
        if not response:
            # If the user hits enter, we return a value of None
            # instead of an empty string.  That way we can determine
            # whether or not a value has changed.
            response = None
        return response


class ConfigureCommand(BasicCommand):
    NAME = 'configure'
    DESCRIPTION = BasicCommand.FROM_FILE()
    SYNOPSIS = ('mng configure')
    EXAMPLES = (
        'To create a new configuration::\n'
        '\n'
        '    $ mng configure\n'
        '    Address Api [None]: localhost\n'
        '    Port Api [None]: 8080\n'
        '    Username Api [None]: user_api\n'
        '    Password API [None]: ********\n'
        '\n'
        'To update just the region name::\n'
        '\n'
        '    $ mng configure\n'
        '    Address Api [localhost]: 192.168.1.2\n'
        '    Port Api [8080]: 8080\n'
        '    Username Api [user_api]: api\n'
        '    Password Api [****]: ********\n'
    )
    SUBCOMMANDS = [
        {'name': 'list', 'command_class': ConfigureListCommand},
        {'name': 'set', 'command_class': ConfigureSetCommand}
    ]

    ARG_TABLE = []

    # If you want to add new values to prompt, update this list here.
    VALUES_TO_PROMPT = [
        # (logical_name, config_name, prompt_text)
        ('address_api', "Address Api"),
        ('port_api', "Port Api"),
        ('username_api', "Username Api"),
        ('password_api', "Passord API"),
    ]

    def __init__(self, prompter=None, config_writer=None):
        super(ConfigureCommand, self).__init__()
        if prompter is None:
            prompter = InteractivePrompter()
        self._prompter = prompter
        if config_writer is None:
            config_writer = ConfigFileWriter()
        self._config_writer = config_writer

    def _run_main(self, parsed_args, parsed_globals):
        # print('ConfigureCommand._run_main.parsed_args: %s' % parsed_args)
        # print('ConfigureCommand._run_main.parsed_globals: %s' % parsed_globals)
        # print('ConfigureCommand._run_main()')
        # Called when invoked with no args "aws configure"
        new_values = {}
        # This is the config from the config file scoped to a specific
        # profile.

        config = {}
        for config_name, prompt_text in self.VALUES_TO_PROMPT:
            current_value = config.get(config_name)
            new_value = self._prompter.get_value(current_value, config_name,
                                                 prompt_text)
            if new_value is not None and new_value != current_value:
                new_values[config_name] = new_value
        base64auth = '%s:%s' % (new_values['username_api'], new_values['password_api'])
        new_values['base64auth'] = base64.b64encode(base64auth.encode("utf-8")).decode('utf-8') #.replace('\n', '')
        config_filename = os.path.expanduser(LOCATION)
        if new_values:
            self._config_writer.update_config(new_values, config_filename)
