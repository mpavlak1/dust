#dust/src/extract/fontsamples.py

# Built-ins
import os
import textwrap

# Package
import __init__

# Additional Packages
from PIL import Image, ImageDraw, ImageFont

def draw_txt(image, text, font, max_w = 40, h0=0, color=(0,0,0)):

    d = ImageDraw.Draw(image)
    w, h = image.size

    for line in textwrap.wrap(text, width=max_w):
        lw, lh = font.getsize(line)
        d.text(((w-lw)/2, h0), line, font=font, fill=color)
        h0+=lh

def str_toimgfile(filepath, text, size=(40,40), background=(255,255,255), fontsize=36, fontfile='arial.ttf'):
    image = Image.new('RGB', size, color=background)
    font = ImageFont.truetype(fontfile, fontsize)
    draw_txt(image, text, font)
    image.save(filepath)

def generate_testfile(testdir, text, filetype='png', fontfile = 'arial.ttf'):
    outfile = os.path.join(testdir,'{}{}{}'.format(text, os.path.extsep, filetype))
    str_toimgfile(outfile, text, fontfile=fontfile)

##f0 = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'test')
##for i in range(10):
##    generate_testfile(f0, str(i))
    
