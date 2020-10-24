from termcolor import colored

TAB = ' ' * 4
HSEP = '-' * 80


def format_text(text, color, attrs=None):
    """Wrap text in ANSI tags
    """
    if not attrs:
        attrs = []
    return colored(text, color, attrs=attrs)


def format_set_tab_size(size):
    """Set the tab size.

    Tabs are converted to spaces, this functions sets the size of a tabulation
    in spaces.

    Arguments:
        size {int} -- [description]
    """
    global TAB
    if size > 0:
        TAB = ' ' * size


def format_dict2str(dictionary):
    """Convert a dictionary recursively into human-readable nested lists

    >>> d = {'a': 1, 'b': 2, 'c': { 4: ['a', 'b'] }}
    >>> print(dict2str(d))
    + a: 1
    + b: 2
    + c:
        + 4: ['a', 'b']

    Arguments:
        dictionary {dict} -- [description]
    """
    text = ""
    for key, value in dictionary.items():
        if isinstance(value, dict):
            text += f"\n> {key}:"
            text += format_dict2str(value).replace("\n", f"\n{TAB}")
        elif isinstance(value, list):
            text += f"\n> {key}: [\n"
            for item in value:
                text += format_dict2str(item).replace("\n", f"\n{TAB}")
                text += "\n"
            text += "\n]\n"
        else:
            text += f"\n> {key}: {value}"
    return text
