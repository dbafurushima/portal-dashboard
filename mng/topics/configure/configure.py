import os

from ...commands import BasicCommand
from .list import ConfigureListCommand
from .set import ConfigureSetCommand
from .writer import ConfigFileWriter
from . import LOCATION, mask_value, profile_to_section


class InteractivePrompter(object):

    def get_value(self, current_value, config_name, prompt_text=''):
        if config_name in ('user_api', 'passwd_api'):
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
    DESCRIPTION = 'configure description rst'
    SYNOPSIS = ('mng configure')
    EXAMPLES = (
        'To create a new configuration::\n'
        '\n'
        '    $ mng configure\n'
        '    IP API [None]: localhost\n'
        '    Port API [None]: 8080\n'
        '    Username API [None]: user_api\n'
        '    Password API [None]: ********\n'
        '\n'
        'To update just the region name::\n'
        '\n'
        '    $ mng configure\n'
        '    IP API [localhost]: 192.168.1.2\n'
        '    Port API [8080]: 8080\n'
        '    Username API [user_api]: api\n'
        '    Passwd API [****]: ********\n'
    )
    SUBCOMMANDS = [
        {'name': 'list', 'command_class': ConfigureListCommand},
        # {'name': 'get', 'command_class': ConfigureGetCommand},
        {'name': 'set', 'command_class': ConfigureSetCommand}
    ]

    ARG_TABLE = [
        {'name': 'order-by', 'help_text': 'This argument does foo bar.', 'required': False}
    ]

    # If you want to add new values to prompt, update this list here.
    VALUES_TO_PROMPT = [
        # (logical_name, config_name, prompt_text)
        ('ip_api', "IP API"),
        ('ip_port', "Port API"),
        ('user_api', "Username API"),
        ('passwd_api', "Passord API"),
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
        print('ConfigureCommand._run_main.parsed_args: %s' % parsed_args)
        print('ConfigureCommand._run_main.parsed_globals: %s' % parsed_globals)
        print('ConfigureCommand._run_main()')
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
        config_filename = os.path.expanduser(LOCATION)
        if new_values:
            self._write_out_creds_file_values(new_values, None)
            self._config_writer.update_config(new_values, config_filename)
    
    def _display_help(self, parsed_args, parsed_globals):
        print('overwirte > ConfigureCommand._display_help()')
    
    def _write_out_creds_file_values(self, new_values, profile_name):
        # credentials file (~/.mng/credentials), see aws/aws-cli#847.
        # post-conditions: ~/.mng/credentials will have the updated credential
        # file values and new_values will have the cred vars removed.
        credential_file_values = {}
        if 'aws_access_key_id' in new_values:
            credential_file_values['aws_access_key_id'] = new_values.pop(
                'aws_access_key_id')
        if 'aws_secret_access_key' in new_values:
            credential_file_values['aws_secret_access_key'] = new_values.pop(
                'aws_secret_access_key')
        if credential_file_values:
            if profile_name is not None:
                credential_file_values['__section__'] = profile_name
            shared_credentials_filename = os.path.expanduser(LOCATION)
            self._config_writer.update_config(
                credential_file_values,
                shared_credentials_filename)
