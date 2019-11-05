# /dust/src/utils/spawn.py

# Built-ins
import subprocess
from subprocess import BELOW_NORMAL_PRIORITY_CLASS
from subprocess import CREATE_NO_WINDOW

# Package
import __init__
from dust.src.errors import NonZeroExitCodeError


def call_nowindow(args):
    if not args: return 0
    exit_code = subprocess.call(args, creationflags = call_nowindow.flag)
    if(exit_code != 0):
        raise NonZeroExitCodeError('Exited with non-zero exit-code {}'.format(exit_code))
    return exit_code
call_nowindow.flag = BELOW_NORMAL_PRIORITY_CLASS + CREATE_NO_WINDOW

