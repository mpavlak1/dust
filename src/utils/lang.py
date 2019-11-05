# /dust/src/utils/lang.py

# Package
import __init__
from dust.src.errors import UnexpectedOptionError


def check_opts(opts, expected_keys):
    """Check that no options are supplied that are not in the expected key list, throws Error on unexpected"""
    _ = tuple(filter(lambda key: key not in expected_keys, opts.keys()))
    if(_):
        print(_)
        raise UnexpectedOptionError(
            'Found unexpected keyword argument options: {}'.format(', '.join(_)))
    
def default_opts(opts, defaults):
    """Update defaults with keyword arguments if supplied"""
    check_opts(opts, defaults.keys())

    for key in defaults:
        opts[key] = opts.get(key, defaults[key])


def switch_statement(case, hash_fn, fn_list):
    """Hashes the case to an index and calls the nth function in list"""
    x = hash_fn(case)
    return fn_list[hash_fn(case)].__call__()
    
