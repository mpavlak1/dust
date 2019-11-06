#dust/src/extract/boxparse.py

# Built-ins
import os

# Package
import __init__
from dust.src.utils.io import spit, slurp

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
        #x,y,w,h = box
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        yield (box, img_arr[y:y+h, x:x+w])

def __homography__(img_arr0, img_arr1):

    g0 = cv2.cvtColor(img_arr0, cv2.COLOR_BGR2GRAY)
    g1 = cv2.cvtColor(img_arr1, cv2.COLOR_BGR2GRAY)

    orb = cv2.ORB_create(__homography__.maxf)
    k0, d0 = orb.detectAndCompute(g0, None)
    k1, d1 = orb.detectAndCompute(g1, None)

    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = sorted(matcher.match(d0, d1, None), key=lambda x: x.distance, reverse=False)
    matches = matches[0:int(len(matches)*__homography__.matchp)]

    p0 = np.zeros((len(matches), 2), dtype=np.float32)
    p1 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        p0[i,:] = k0[match.queryIdx].pt
        p1[i,:] = k1[match.trainIdx].pt

    h, mask = cv2.findHomography(p0, p1, cv2.RANSAC)

    height, width, channels = img_arr1.shape
    adj_arr = cv2.warpPerspective(img_arr0, h, (width, height))

    return adj_arr, h
__homography__.maxf = 150000
__homography__.matchp = 0.03

def split_bybox(imgfile, outdir, imgtype = 'png', boxs = None, reference_imgfile = None):
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
        cv2.imwrite(outfile, loc_box[1])
        spit(boxloc_file, '{}\t{}\n'.format(outfile, str(loc_box[0])))
