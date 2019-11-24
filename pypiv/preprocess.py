import numpy as np

#from scipy.misc import imread
from imageio import imread
from scipy.ndimage import gaussian_filter
from skimage.exposure import equalize_adapthist

def subtract_background2file(images, output_file):
    '''
    Compute Background from image list and save it as numpy array
    '''
    data = imread(images[0])
    for  img in images:
        data = np.min(np.array([data, imread(img)]), axis=0)
    np.save(output_file, data)

def subtract_background(images):
    '''
    Compute Background from image list and save it as numpy array
    '''
    readin  = False
    if isinstance(images[0],str):
        bg = imread(images[0])
        readin = True
    else:
        bg = np.copy(images[0])
    for  img in images:
        if readin:
            bg = np.min(np.array([bg, imread(img)]), axis=0)
        else:
            bg = np.min(np.array([bg, img]), axis=0)
    imgs    = []
    for img in images:
        if readin:
            imgs.append(imread(img)-bg)
        else:
            imgs.append(img-bg)
    return np.array(imgs),bg

def subtract_background_pair(images):
    '''
    Compute Background from image list and save it as numpy array
    '''
    readin  = False
    if isinstance(images[0],str):
        bg = np.min(np.array([imread(images[0]), imread(images[1])]), axis=0)
    else:
        bg = np.min(np.array([images[0], images[1]]), axis=0)
    imgs    = []
    for img in images:
        if readin:
            imgs.append(imread(img)-bg)
        else:
            imgs.append(img-bg)
    return np.array(imgs),bg


def cap_image(img, cap_min, cap_max):
    img[img<cap_min] = cap_min
    img[img>cap_max] = cap_max
    return img

def highpass_filter(img, sigma=3):
    lowpass = gaussian_filter(img, 3)
    return img - lowpass

def clahe_normalization(img, kernel_size=3, nbins=1024, clip_limit=0.3):
    '''Contrast Limited Adaptive Histogram Equalization (CLAHE).'''
    return equalize_adapthist(img, kernel_size, nbins, clip_limit)



