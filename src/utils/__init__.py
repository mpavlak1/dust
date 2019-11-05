# /dust/src/utils/__init__.py

import os
import sys

if not '__file__' in globals():
    __file__ = os.path.join(os.path.abspath('.'), '__init__.py')

def __setpaths__(level):

    PATHS = [os.path.abspath('.')]
    for i in range(level):
        PATHS.append(os.path.split(PATHS[-1])[0])

    for PATH in PATHS:
        if(PATH not in sys.path):
            sys.path.append(PATH)

__setpaths__(3)

import dust.src.utils
