# /dust/src/extract/images.py

# Built-in
import os

# Package
import __init__

from dust.src.utils.filepaths import as_filetype

# Additional Packages
from PIL import Image

def monochrome(imgfile, threshold = 150, outfile = None):
    """Convert all pixels in image to either Black or White based on threshold value"""
    #Origonal imgfile will be overwritten if no outfile specified

    i = Image.open(imgfile)
    fn = lambda x: 255 if x > threshold else 0

    r = i.convert('L').point(fn, mode='1')
    r.save(outfile if outfile else imgfile)

    
def convert(imgfile, filetype, outfile=None):
    """Convert imagefile to different image file type"""
    Image.open(imgfile).save(as_filetype(outfile or imgfile, filetype))
   


f0 = 'C:/Users/michael.pavlak/Desktop/irs_sampleform_img-dump/irs_sampleform-001.png'
f00 = Image.open(f0)

##from PIL import Image
##import numpy as np
##
##w, h = 512, 512
##data = np.zeros((h, w, 3), dtype=np.uint8)
##data[256, 256] = [255, 0, 0]
##img = Image.fromarray(data, 'RGB')
##img.save('my.png')
##img.show()


def img_subsec(imgArr, outfile, format_='RGB'):
    imgObj = Image.fromarray(imgArr, format_)
    imgObj.save(outfile)
    #imgObj.show()

import numpy as np
def subArr(arr0, n, m, start_y=0, start_x=0):
    data = np.zeros((n, m, 3), dtype=np.uint8)

    for y in range(n):
        for x in range(m):
            p = arr0[x+start_x,y+start_y]
            data[y,x,0] = p[0]
            data[y,x,1] = p[1]
            data[y,x,2] = p[2]
    return data

def itr_img(imgObj):
    xmax = imgObj.width
    ymax = imgObj.height

    px = imgObj.load()
    for x in range(xmax):
        for y in range(ymax):
            yield [x,y, px[x,y]]


def seek_img(imgItr, dry_thresh = 20):

    p0 = None
    dry = 0

    for cord in imgItr:
        if(cord[2] == (255,255,255)):
            continue
        else:
            p0 = cord
            break

    for cord in imgItr:
        if(dry >= dry_thresh): break
        if(cord[2] == (255,255,255)):
            dry+=1
            continue
    return [p0, cord]
        


def qqq():
    m = subArr(f00.load(), 105, 10, start_y=1664, start_x=98)
    img_subsec(m, 'C:/Users/michael.pavlak/Desktop/out.png')
    
