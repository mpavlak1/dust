# /dust/test/__init__.py

import os
import sys

if not '__file__' in globals():
    __file__ = os.path.join(os.path.abspath('.'), '__init__.py')

try:
    with open(os.path.join(os.path.split(__file__)[0],'paths.txt')) as r:
        for line in r.readlines():

            key, path = line.strip().split('\t')

            if(key.upper() == 'SRC'):  
                if(path not in sys.path and os.path.exists(path)):
                    sys.path.append(path)
            else:
                if(os.path.exists(path)):
                    os.environ[key.upper()] = path
except FileNotFoundError: pass
    

def __setpaths__(level):

    PATHS = [os.path.abspath('.')]
    for i in range(level):
        PATHS.append(os.path.split(PATHS[-1])[0])

    for PATH in PATHS:
        if(PATH not in sys.path):
            sys.path.append(PATH)

__setpaths__(2)
