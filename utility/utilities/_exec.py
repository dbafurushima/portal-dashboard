import os
import re
import sys
import json
import time
import sched
import psutil
import pprint
import datetime
import tempfile

from .graph import get_graph_by_id, get_graph_by_uid, get_index_graph, put_data_to_graph
from .utils import debug, save_working_status
from .utils_exceptions import ChoicePerTimeIsNotValid, GraphDoesNotExist
from .utils_constants import (CHOICES_PER_TIME, DEFAULT_BACKUP, DEFAULT_THROW, DEFAULT_TURN,
    CHOICES_PRIORITY, DEFAULT_WORKER_PATH)
from ._load_work import WORKER

INDEX = 0


def execute(
        resource,
        graph: int or str,
        turn: int = DEFAULT_TURN,
        per: str = 'second', # CHOICES_PER_TIME.keys()[3],
        backup: bool = DEFAULT_BACKUP,
        throw: bool = DEFAULT_THROW,
        priority: int = CHOICES_PRIORITY[0],
        sch: sched.scheduler = None) -> None:

    def _exec(resource, graph, format, bk: bool = False):
        global INDEX
        INDEX += 1

        if resource.lower() == 'cpu':
            value = psutil.cpu_percent(interval=1)
        if resource.lower() == 'mem':
            value = psutil.virtual_memory().percent

        data_post = {
            'index': INDEX,
            'chart': graph,
            'value': '%s,%s' % (
                datetime.datetime.now().strftime(format), value
                )}
        put_data_to_graph(data_post)

    try:
        obj_graph = get_graph_by_id(graph, throw=True) \
            if not re.match(r'^[0-9a-f]{4}_', '%s' % graph) \
            else get_graph_by_uid(graph, throw=True)
    except GraphDoesNotExist as err:
        sys.exit('ERROR: %s' % err)

    strtime = json.loads(obj_graph.get('schema'))[0].get('format')
    index = get_index_graph(obj_graph.get('id'))
    INDEX = index
    # index = iter(
    #     list(
    #         range(
    #             index+1, index + (turn + 1)
    #         )
    #     )
    # )

    sch = sched.scheduler(time.time, time.sleep) if sch is None else sch

    try:
        wait = CHOICES_PER_TIME[per]
    except KeyError:
        raise ChoicePerTimeIsNotValid()

    turn, loop = (1, True) if turn <= 0 else (turn, False)

    def __start_running():
        debug('starting process with pid %s' % os.getpid())
        while True:
            for i in range(turn):
                sch.enter(
                    wait * i,
                    priority,
                    _exec,
                    argument=(
                        resource, obj_graph.get('id'), strtime, backup
                    )
                )
            sch.run()
            if not loop: break
        debug('ending process with pid %s' % os.getpid())

    debug('schedule cpu metrics to be sent %s times within a interval %s' % (turn, per))

    newpid = os.fork()

    if newpid == 0:
        __start_running()