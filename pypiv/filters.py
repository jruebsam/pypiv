import numpy as np

from numpy.lib.stride_tricks import as_strided
from scipy.ndimage import median_filter
from scipy.interpolate import CloughTocher2DInterpolator as intp

from skimage.filters.rank import median
from skimage.morphology import disk
from scipy.ndimage import median_filter as mf

def median_filter(piv, size=2):
     piv.u = mf(piv.u, footprint=disk(size))
     piv.v = mf(piv.v, footprint=disk(size))

def replace_outliers(piv):
    mask = np.isnan(piv.u) + np.isnan(piv.v)
    piv.u = replace_field(piv.u, mask)
    piv.v = replace_field(piv.v, mask)

def replace_field(f, mask):
    lx, ly = f.shape
    x, y = np.mgrid[0:lx, 0:ly]
    C = intp((x[~mask],y[~mask]),f[~mask], fill_value=0)
    return C(x, y)

def outlier_from_local_median(piv, treshold=2.0):
    '''
    Implementation of a local median filter according to
    "J. Westerweel, F. Scarano, Universalo outlier detection for PIV data,\
            Experiments in Fluids, 2005"
    Input:
        u: x-component of velocity field with shape NxN
        v: x-component of velocity field with shape NxN
        treshold: threshold for identfying outliers
    Returns:
        m: Boolean masking function where 1 corresponds to an outliers
    '''
    u_res = get_normalized_residual(piv.u)
    v_res = get_normalized_residual(piv.v)
    res_total = np.sqrt(u_res**2 + v_res**2)
    mask =  res_total > treshold
    piv.u[mask] = np.nan
    piv.v[mask] = np.nan


def get_normalized_residual(f, epsilon=0.1):
    '''
    Compute Residual for a Flow field
    '''
    lx, ly = f.shape
    fn = np.pad(f, (1, 1), 'edge')

    uis     = np.zeros((lx*ly, 8))
    um, rm  = np.zeros((lx*ly)), np.zeros((lx*ly))

    mapping = [(0, 0), (1, 0), (2, 0), (0, 1), (2, 1), (0, 2), (1, 2), (2, 2)]
    for i, (k, l) in enumerate(mapping):
        uis[:, i] = np.copy(fn[k:k+lx, l:l+ly]).flatten()

    uis = np.sort(uis, 1)
    um  = np.copy(uis[:, 4])[:, np.newaxis]

    ris = np.abs(uis - um)
    rm  = np.sort(ris, 1)[:, 4][:, np.newaxis]

    return np.abs((f - um.reshape((lx, ly)))/(rm.reshape((lx, ly)) + epsilon))
