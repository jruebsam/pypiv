import numpy as np
from numpy import log

def find_subpixel_peak(corr, subpixel_method = 'gaussian'):
    """
    Find subpixel approximation of the correlation peak.

    Parameters
    ----------
    corr : np.ndarray - the correlation map.

    subpixel_method : string
         one of the following methods to estimate subpixel location of the peak:
         'centroid' [replaces default if correlation map is negative],
         'gaussian' [default if correlation map is positive],
         'parabolic'.

    Returns
    -------
    subp_peak_position : two elements tuple
        the fractional row and column indices for the sub-pixel
        approximation of the correlation peak.
    """

    # initialization
    default_peak_position = (corr.shape[0]/2,corr.shape[1]/2)

    # the peak locations
    peak_i, peak_j = np.unravel_index(corr.argmax(), corr.shape)
    peak_max = np.max(corr)

    try:
        # the peak and its neighbours: left, right, down, up
        c  = corr[peak_i  , peak_j  ]
        cl = corr[peak_i-1, peak_j  ]
        cr = corr[peak_i+1, peak_j  ]
        cd = corr[peak_i  , peak_j-1]
        cu = corr[peak_i  , peak_j+1]

        # gaussian fit
        if np.any ( np.array([c,cl,cr,cd,cu]) < 0 ) and subpixel_method == 'gaussian':
            subpixel_method = 'centroid'

        try:
            if subpixel_method == 'centroid':
                peak_xpos = ((peak_i - 1)*cl + peak_i*c + (peak_i + 1)*cr)/(cl + c + cr)
                peak_ypos = ((peak_j - 1)*cd + peak_j*c + (peak_j + 1)*cu)/(cd + c + cu)

            elif subpixel_method == 'gaussian':
                peak_xpos = peak_i +  (log(cl) - log(cr))/(2*log(cl) - 4*log(c) + 2*log(cr))
                peak_ypos = peak_j +  (log(cd) - log(cu))/(2*log(cd) - 4*log(c) + 2*log(cu))

            elif subpixel_method == 'parabolic':
                peak_xpos = peak_i +  (cl - cr)/(2*cl -4*c + 2*cr)
                peak_ypos = peak_j +  (cd - cu)/(2*cd -4*c + 2*cu)

            subp_peak_position = (peak_xpos, peak_ypos)
        except:
            subp_peak_position = default_peak_position

    except IndexError:
            subp_peak_position = default_peak_position
    return subp_peak_position[0], subp_peak_position[1]

