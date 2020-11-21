import click
from .utils_constants import (CHOICES_TYPE_RESOURCE, CHOICES_PER_TIME, DEFAULT_CLI_ENABLE_BACKUP)


@click.command(name='utils', help='Utility to feed graphs with data.')
@click.version_option('0.0.1', '-v', '--version', message='%(version)s')
@click.argument('resource', default='cpu', type=click.Choice(CHOICES_TYPE_RESOURCE, case_sensitive=False))
@click.option('--config-file', default=None, type=click.Path(), help=('Configuration file with resource access credentials.'))
@click.option('-d', '--debug', count=True, type=click.IntRange(0, 3),
              help='Enable debug mode for greater verbosity. Contains 3 different levels.')
@click.option('-p', '--per', default='second', type=click.Choice(CHOICES_PER_TIME.keys(), case_sensitive=False),
              help=('Will data be sent at an interval of...'))
@click.option('-t', '--turn', default=5, type=int,
              help=('Number of data you are recovering. To get the metrics while the tool is running, just choose "0".'))
@click.option('--backup/--no-backup', default=DEFAULT_CLI_ENABLE_BACKUP, is_flag=True,
              help=('If the sending of any information fails, the data will be saved in a temporary file.'))
def cli(resource, config_file, verbose, per, turn):
    pass