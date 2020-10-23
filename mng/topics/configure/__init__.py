from pathlib import Path

NOT_SET = '<not set>'
PREDEFINED_SECTION_NAMES = ('preview', 'plugins')
_WHITESPACE = ' \t'
LOCATION = Path.home().joinpath('.config', 'mng', 'mng.yml')


class ConfigValue(object):

    def __init__(self, value, config_type, config_variable):
        self.value = value
        self.config_type = config_type
        self.config_variable = config_variable

    def mask_value(self):
        if self.value is NOT_SET:
            return
        self.value = mask_value(self.value)


class SectionNotFoundError(Exception):
    pass


def mask_value(current_value):
    if current_value is None:
        return 'None'
    else:
        return ('*' * 16) + current_value[-4:]


def profile_to_section(profile_name):
    """Converts a profile name to a section header to be used in the config."""
    # if any(c in _WHITESPACE for c in profile_name):
    #     profile_name = shlex_quote(profile_name)
    return 'profile %s' % profile_name
