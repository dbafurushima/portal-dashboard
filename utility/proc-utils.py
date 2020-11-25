import click
import psutil

FILENAME = 'mngutils.py'

def _list_procs(isdebug: bool = False):
    list_of_process = []
    for pid in psutil.pids():
        p = psutil.Process(pid=pid)
        if p.name().lower().startswith('python'):
            try:
                cmdline = p.cmdline()
                if FILENAME in cmdline:
                    list_of_process.append(p)
                    if isdebug:
                        print('[%s] >> %s' % (p.pid, ' '.join(cmdline)))
            except (FileNotFoundError, psutil.NoSuchProcess):
                pass
    return list_of_process

@click.group(name='manage', help='Manage Python processes created by the "utility" tool.')
@click.option('-d', '--debug', count=True, type=click.IntRange(0, 3),
              help='Enable debug mode for greater verbosity. Contains 3 different levels.')
def cli(debug):
    pass

@cli.command(name='list', help='Lists all processes (pid and cmd) of the tool currently running.')
def _list():
    list_of_process = _list_procs(isdebug=True)
    if not list_of_process:
        print('! No running processes.')

@cli.command(name='kill', help='Kills a tool process that is currently running.')
@click.argument('pid', type=int, metavar='<pid>')
def kill(pid):
    try:
        p = psutil.Process(pid=pid)
        p.kill()
    except psutil.NoSuchProcess:
        print('! Process with pid "%s" not exists.' % pid)

@cli.command(name='killall', help='Kills all currently running tool processes.')
def killall():
    procs = _list_procs()
    if not procs:
        print('! No running processes.')
        return

    try:
        for proc in procs:
            print(' - kill process "%s"' % proc.pid)
            proc.kill()
    except psutil.NoSuchProcess:
        print('! psutil.NoSuchProcess')


if __name__ == '__main__':
    cli()