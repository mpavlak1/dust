# /dust/src/extract/tesseract.py

# Built-ins
import os
from os import environ
import subprocess

#Package
import __init__
from dust.src.utils.lang import default_opts, switch_statement
from dust.src.utils.spawn import call_nowindow
from dust.src.utils.io import spit

def tesseractOCRsingle(imgfile, outfile, **opts):
    default_opts(opts, dict(tesseractOCRsingle.defaultopts))
    
    #Check if file exists and not overwrite
    args = switch_statement(opts, lambda opts: int(not opts['overwrite'] and os.path.exists(outfile)),
                            [lambda: [environ['tesseract'], imgfile, outfile,
                              '--oem', str(opts['oem']), '--psm', str(opts['psm'])],
                                      #,'-l', opts['language']],
                             lambda: []])                   
    #Spawn subprocess
    try:
        return call_nowindow(args)
    except Exception as e:
        print(e)
        print(args)
        os.getcwd()

tesseractOCRsingle.defaultopts = {'oem':1, 'psm':1, 'language':'eng', 'overwrite':False}

##def tesseractOCRbatch(imgdir, outfile, **opts):
##
##    input_file = os.path.join(imgdir, 'input_file.txt')
##    default_opts(opts, dict(tesseractOCRbatch.defaultopts))
##
##    try: os.remove(input_file)
##    except FileNotFoundError: pass
##
##    filenames = map(lambda x: os.path.join(imgdir, x), os.listdir(imgdir))
##    spit(input_file, '\n'.join(filenames), mode='w')
##
##    args = [environ['tesseract'], input_file, outfile,
##            '--oem', str(opts['oem']), '--psm', str(opts['psm'])]
##    
##    return call_nowindow(args)
##tesseractOCRbatch.defaultopts = {'oem':1, 'psm':1, 'language':'eng', 'overwrite':False}
