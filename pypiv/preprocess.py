import numpy as np

from scipy.misc import imread
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



