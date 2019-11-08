# /dust/src/utils/io.py

# Built-ins
import os

# Package
import __init__

def spit(filepath, msg, mode='a'):
    with open(filepath, mode=mode) as w:
        w.write(msg)

def slurp(filepath):
    with open(filepath) as w:
        return list(w.readlines())

