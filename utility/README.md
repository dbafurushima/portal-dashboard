### ``mngutils.py``

```
$ python mngutils.py --help

Usage: mngutils.py [OPTIONS] [<graph-id>|<graph-uid>] [[cpu|mem]]

  Utility to feed graphs with data, in an automated way.

Options:
  -v, --version                   Show the version and exit.
  --config-file PATH              Configuration file with resource access
                                  credentials.

  -d, --debug                     Enable debug mode for greater verbosity.
                                  Contains 3 different levels.

  -p, --per [week|day|hour|minute|second]
                                  Will data be sent at an interval of...
  -t, --turn INTEGER              Number of data you are recovering. To get
                                  the metrics while the tool is running, just
                                  choose "0".

  --backup / --no-backup          If the sending of any information fails, the
                                  data will be saved in a temporary file.

  --help                          Show this message and exit.
```

### ``proc-utils.py``

```
$ python proc-utils.py --help

Usage: proc-utils.py [OPTIONS] COMMAND [ARGS]...

  Manage Python processes created by the "utility" tool.

Options:
  -d, --debug  Enable debug mode for greater verbosity. Contains 3 different
               levels.
  --help       Show this message and exit.

Commands:
  kill     Kills a tool process that is currently running.
  killall  Kills all currently running tool processes.
  list     Lists all processes (pid and cmd) of the tool currently running.
```