import os
import pprint
import psutil

pids = psutil.pids()

for pid in pids:
    p = psutil.Process(pid=pid)
    pprint.pprint(p.name())
