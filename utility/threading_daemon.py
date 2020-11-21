from multiprocessing import Process
import multiprocessing as mp
import time
import sys
import multiprocessing

p = multiprocessing.Process(target=time.sleep, args=(1000,))
print(p, p.is_alive())
p.start()
print('z')
time.sleep(1)