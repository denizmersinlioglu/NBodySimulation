import time
import datetime
import math
import random


def millis():
    return int(round(time.time() * 1000))


def exp(value):
    return -math.log(1 - random.random()) / value


def signum(int):
    if(int < 0):
        return -1
    elif(int > 0):
        return 1
    else:
        return int
