#dust/src/extract/boxparse.py

# Built-ins
import os

# Package
import __init__
from dust.src.utils.io import spit, slurp
from dust.src.extract.images import homography as __homography__

# Additional Packages
import numpy as np
import cv2

def seek_boxes(img_arr, iterations=3, alpha=0.5):

    thresh, img_mono = cv2.threshold(img_arr, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    img_mono = 255-img_mono

    kern_len = np.array(img_arr).shape[1]//40
    kern = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
    v_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kern_len))
    h_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (kern_len, 1))

    v_erode = cv2.erode(img_mono, v_kern, iterations=iterations)
    v_lines = cv2.dilate(v_erode, v_kern, iterations=iterations)

    h_erode = cv2.erode(img_mono, h_kern, iterations=iterations)
    h_lines = cv2.dilate(h_erode, h_kern, iterations=iterations)

    cross_section = cv2.addWeighted(v_lines, alpha, h_lines, 1.0-alpha, 0.0)
    cross_section = cv2.erode(~cross_section, kern, iterations=iterations)

    thresh, cross_sec = cv2.threshold(cross_section, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    contours = cv2.findContours(cross_sec, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0] #rectangles are first in list

    for c in contours:
        yield cv2.boundingRect(c)
    
def parse_boxes(img_arr, boxes):
    '''generator of tuples of box location and image data within the box borders'''
    for box in boxes:
        x,y,w,h = box
        yield (box, img_arr[y:y+h, x:x+w])

def split_chars(img_arr, max_h = 40, max_w = 40, min_h = 4, min_w = 10, upscale_factor = 5):

    _,img_arr = cv2.threshold(img_arr,127,255,cv2.THRESH_BINARY)

    contours = cv2.findContours(img_arr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    contours.sort(key=lambda x: cv2.boundingRect(x)[0])

    for i,cont in enumerate(contours):
        x,y,w,h = cv2.boundingRect(cont)
        if((w < max_w and w > min_w) and (h < max_h and h > min_h)):
            yield ((x,y,w,h), cv2.resize(img_arr[y:y+h,x:x+w], (w*upscale_factor,h*upscale_factor),
                                         interpolation=cv2.INTER_AREA))


def remove_nonchar_noise(img_arr, max_h = 40, max_w = 40, min_h = 1, min_w = 1):
    b = img_arr.copy()
    b[::] = 255

    char_itr = split_chars(img_arr, max_h=max_h, max_w=max_w, min_h=min_h, min_w=min_w, upscale_factor=1)
    for box, char_arr in char_itr:
        x,y,w,h = box
        b[y:y+h,x:x+w] = img_arr[y:y+h,x:x+w]
    return b

def split_bybox(imgfile, outdir, imgtype = 'png', boxs = None, reference_imgfile = None, noisefilter_fn = remove_nonchar_noise):
    '''Split an image file by identified box locations'''

    if(reference_imgfile):
        #align imgfile to reference image if give to ensure any pre-defined boxes align as expected
        ref_img = cv2.imread(reference_imgfile, cv2.IMREAD_COLOR)

        img_arr = cv2.imread(imgfile, cv2.IMREAD_COLOR)
        img_arr = cv2.cvtColor(__homography__(img_arr, ref_img)[0], cv2.COLOR_BGR2GRAY)
    else:
        img_arr = cv2.imread(imgfile,0)
    
    locs_boxs = parse_boxes(img_arr, boxs or seek_boxes(img_arr))

    boxloc_file = os.path.join(outdir,'box_legend.txt')
    for i,loc_box in enumerate(locs_boxs):
        outfile = os.path.join(outdir,'{}.{ft}'.format(i,ft=imgtype))
       
        cv2.imwrite(outfile, noisefilter_fn(loc_box[1]))
        spit(boxloc_file, '{}\t{}\n'.format(outfile, str(loc_box[0])))



