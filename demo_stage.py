import sys 
import time

def flush_then_wait():
    sys.stdout.flush()
    time.sleep(5)

stages = ["       Non-Seizure", "       Seizure-onset", "       Seizure-onset", "\tSeizure"]

for i in stages:
    sys.stdout.write(i)
    flush_then_wait()
