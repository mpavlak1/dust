# /dust/src/extract/images.py

# Built-in
import os

# Package
import __init__

from dust.src.utils.filepaths import as_filetype

# Additional Packages
from PIL import Image
import numpy as np
import cv2

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

def homography(img_arr0, img_arr1):
    ##img_arr0 is the image to be adjusted, img_arr1 is the reference
    g0 = cv2.cvtColor(img_arr0, cv2.COLOR_BGR2GRAY)
    g1 = cv2.cvtColor(img_arr1, cv2.COLOR_BGR2GRAY)

    orb = cv2.ORB_create(homography.maxf)
    k0, d0 = orb.detectAndCompute(g0, None)
    k1, d1 = orb.detectAndCompute(g1, None)

    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = sorted(matcher.match(d0, d1, None), key=lambda x: x.distance, reverse=False)
    matches = matches[0:int(len(matches)*homography.matchp)]

    p0 = np.zeros((len(matches), 2), dtype=np.float32)
    p1 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        p0[i,:] = k0[match.queryIdx].pt
        p1[i,:] = k1[match.trainIdx].pt

    h, mask = cv2.findHomography(p0, p1, cv2.RANSAC)

    height, width, channels = img_arr1.shape
    adj_arr = cv2.warpPerspective(img_arr0, h, (width, height))

    return adj_arr, h
homography.maxf = 150000
homography.matchp = 0.05


def image_similarity(img_arr0, img_arr1, method = cv2.TM_CCOEFF_NORMED, adjust_image = True):
    '''Return the percent simialrity between img0 and img1'''
    if(adjust_image):
        img_arr0 = homography(img_arr0, img_arr1)[0]

    img_arr0 = cv2.cvtColor(img_arr0,cv2.COLOR_BGR2GRAY)
    img_arr1 = cv2.cvtColor(img_arr1,cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(img_arr0, img_arr1, method)
    return cv2.minMaxLoc(res)[1]





