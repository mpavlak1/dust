# /dust/src/extract/ghostscript.py

# Built-ins
from os import environ

# Package
import __init__
from dust.src.extract import images
from dust.src.utils import filepaths as fps
from dust.src.utils.lang import default_opts, switch_statement
from dust.src.utils.spawn import call_nowindow

assert 'ghostscript' in environ

def pdf_toimgs(pdffile, **opts):
    _pages=opts.pop('pages') if 'pages' in opts else None
    
    default_opts(opts, dict(pdf_toimgs.defaultopts))
    assert opts['img_format'] in pdf_toimgs.switch.keys(), \
           'Invalid image format: {}'.format(opts['img_format'])

    assert opts['tiff_opt'] in pdf_toimgs.tiff_opts, \
           'Invaid TIFF format: {}'.format(opts['tiff_opt'])
    
    outdir = fps.as_directory(pdffile,'_img-dump')

    fps.make_directory(outdir)
    
    args = switch_statement(opts, lambda opts: pdf_toimgs.switch[opts['img_format']],
                            [lambda: ['-sDEVICE=png16m',
                                      '-r{}'.format(opts['resolution']),
                                      '-dDownScaleFactor={}'.format(opts['down_scale_factor'])],
                             lambda: ['-sDEVICE=jpeg',
                                      '-dJPEGQ={}'.format(opts['jpegq']),
                                      '-dQFactor=1'.format(opts['qfactor'])],
                             lambda: ['-SDEVICE=tiff{}'.format(opts['tiff_opts']),
                                      '-r{}'.format(opts['resolution']),
                                      '-dDownScaleFactor={}'.format(opts['down_scale_factor'])]]) \
                                      +  ['-o{}-%03d.{}'.format(
                                          fps.topaths(outdir, fps.basename(pdffile,False)),
                                          opts['img_format']),pdffile]
    if(_pages):
        args.insert(0, '-sPageList={}'.format(','.join(map(str,_pages))))
##        args.append('-dFirstPage={}'.format(_page))
##        args.append('-dLastPage={}'.format(_page))
##    print(args)

    return call_nowindow([environ['ghostscript']] + args)

pdf_toimgs.gsargs = [environ['ghostscript'], '-q', '-dBATCH', '-dNOPAUSE', '-dQUIET']
pdf_toimgs.opts = ['img_format','jpegq', 'qfactor', 'down_scale_factor', 'resolution', 'tiff_opt']
pdf_toimgs.defaultopts = dict(zip(pdf_toimgs.opts, ['png', 100, 1, 1, 900, 'g4']))
pdf_toimgs.switch = {'png':0,'jpeg':1,'tiff':2}
pdf_toimgs.tiff_opts = ['gray','12nc','24nc','48nc','32nc','64nc','sep','sep1',
                        'scaled','scaled4','scaled8','scaled24','scaled32',
                        'crle','g3','g32d','g4','lzw','pack']
