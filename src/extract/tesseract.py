# /dust/src/extract/tesseract.py

# Built-ins
import os
from os import environ
import subprocess

#Package
import __init__
from dust.src.utils.lang import default_opts, switch_statement
from dust.src.utils.spawn import call_nowindow
from dust.src.extract.images import monochrome


def preprocess_img(imgfile):
    return monochrome(imgfile)


def tesseractOCRsingle(imgfile, outfile, **opts):
    default_opts(opts, dict(tesseractOCRsingle.defaultopts))

    #Check if file exists and not overwrite
    args = switch_statement(opts, lambda opts: int(not opts['overwrite'] and os.path.exists(outfile)),
                            [lambda: [environ['tesseract'], imgfile, outfile,
                              '--oem', str(opts['oem']), '--psm', str(opts['psm']),
                                      '-l', opts['language']],
                             lambda: []])                   
    #Spawn subprocess
    print(args)
    return call_nowindow(args)

tesseractOCRsingle.defaultopts = {'oem':1, 'psm':1, 'language':'eng', 'overwrite':False}
