import numpy as np

from numpy.lib.stride_tricks import as_strided
from scipy.ndimage import median_filter
from scipy.interpolate import CloughTocher2DInterpolator as intp

from skimage.filters.rank import median
from skimage.morphology import disk
from scipy.ndimage import median_filter as mf

def median_filter(f, size=2):
    return mf(f, footprint=disk(size))

def replace_outliers(u, v, mask):
    u_out = replace_field(u, mask)
    v_out = replace_field(v, mask)
    return u_out, v_out

def replace_field(f, mask):
    lx, ly = f.shape
    x, y = np.mgrid[0:lx, 0:ly]
    C = intp((x[~mask],y[~mask]),f[~mask], fill_value=0)
    return C(x, y)

def local_median_filter(u, v, treshold=2.0):
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
    u_res = get_normalized_residual(u)
    v_res = get_normalized_residual(v)
    res_total = np.sqrt(u_res**2 + v_res**2)
    return res_total > treshold


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

def local_median( u, v, u_threshold, v_threshold, size=1 ):
    """Eliminate spurious vectors with a local median threshold.

    This validation method tests for the spatial consistency of the data.
    Vectors are classified as outliers and replaced with Nan (Not a Number) if
    the absolute difference with the local median is greater than a user
    specified threshold. The median is computed for both velocity components.

    Parameters
    ----------
    u : 2d np.ndarray
        a two dimensional array containing the u velocity component.

    v : 2d np.ndarray
        a two dimensional array containing the v velocity component.

    u_threshold : float
        the threshold value for component u

    v_threshold : float
        the threshold value for component v

    Returns
    -------
    u : 2d np.ndarray
        a two dimensional array containing the u velocity component,
        where spurious vectors have been replaced by NaN.

    v : 2d np.ndarray
        a two dimensional array containing the v velocity component,
        where spurious vectors have been replaced by NaN.

    mask : boolean 2d np.ndarray
        a boolean array. True elements corresponds to outliers.

    """

    um = median_filter( u, size=2*size+1 )
    vm = median_filter( v, size=2*size+1 )

    ind = (np.abs( (u-um) ) > u_threshold) | (np.abs( (v-vm) ) > v_threshold)

    ind = (um*u + v*vm) < 0

    u[ind] = np.nan
    v[ind] = np.nan

    mask = np.zeros(u.shape, dtype=bool)
    mask[ind] = True

    return u, v, mask
