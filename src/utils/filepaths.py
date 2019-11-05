# /dust/src/utils/filepaths.py

# Built-ins
import os

# Package
import __init__

def basename(filepath, ft=True):
    return os.path.basename(filepath) if ft else os.path.splitext(os.path.basename(filepath))[0]

def as_filetype(filepath, filetype):
    """Convert the file type extension to new filetype extension"""

    return os.path.extsep.join([os.path.splitext(filepath)[0],
                                filetype.replace(os.path.extsep,'')])

def rem_filetype(filepath):
    return os.path.splitext(filepath)[0]


def as_directory(filepath, dirext='_'):
    return os.path.join(os.path.dirname(filepath),
                        ''.join([os.path.splitext(os.path.basename(filepath))[0],dirext]))

def make_directory(directory):
    os.makedirs(directory, exist_ok=True)

def get_filetype(filepath):
    """Returns the file extension of the filepath"""
    return os.path.splitext(filepath)[1].split(os.path.extsep)[-1].lower()

def extend_name(filepath, ex):
    _ = list(os.path.splitext(filepath))
    _.insert(-1, ex)
    return os.path.join(*_)

def topaths(*paths): 
    return os.path.join(*paths)

  

