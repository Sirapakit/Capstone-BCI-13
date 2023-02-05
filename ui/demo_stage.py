import sys 
import time

def flush_then_wait():
    sys.stdout.flush()
    time.sleep(30)

stages = ["\tNon-Seizure", "\tSeizure-onset", "\t   Seizure"] # stages

for i in stages:
    sys.stdout.write(i)
    flush_then_wait()
