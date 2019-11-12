# /dust/src/extract/images.py

# Built-in
import os

# Package
import __init__

from dust.src.utils.filepaths import as_filetype

# Additional Packages
import numpy as np
import cv2

def homography(img_arr0, img_arr1):
    ##img_arr0 is the image to be adjusted, img_arr1 is the reference
    g0 = cv2.cvtColor(img_arr0, cv2.COLOR_BGR2GRAY)
    g1 = cv2.cvtColor(img_arr1, cv2.COLOR_BGR2GRAY)

    orb = cv2.ORB_create(homography.maxf)
    k0, d0 = orb.detectAndCompute(g0, None)
    k1, d1 = orb.detectAndCompute(g1, None)

    #cv2.NORM_HAMMING
    #matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_FLANNBASED)
    d0 = np.float32(d0)
    d1 = np.float32(d1)

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



def __imgarr__(imgfile, mode=6):
    arr = cv2.imread(imgfile, mode)
    assert arr is not None

    return arr

def image_similarity(img_arr0, img_arr1, method = cv2.TM_CCOEFF_NORMED, adjust_image = True):
    '''Return the percent simialrity between img0 and img1'''
    if(adjust_image):
        img_arr0 = homography(img_arr0, img_arr1)[0]

    img_arr0 = cv2.cvtColor(img_arr0,cv2.COLOR_BGR2GRAY)
    img_arr1 = cv2.cvtColor(img_arr1,cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(img_arr0, img_arr1, method)
    return cv2.minMaxLoc(res)[1]





