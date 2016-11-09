import matplotlib as mt
backend = mt.get_backend()
if backend == 'agg':
    mt.use('TKagg')
import pypiv
import numpy as np
import matplotlib.pyplot as plt
from glob import glob

def main():
    imgs = ['images/finger1.png', 'images/finger2.png']
    frames = [plt.imread(x) for x in imgs]
    frame_a, frame_b = frames[0], frames[1]

    frame_a_inv = np.copy(frame_a[::-1,::-1])
    frame_b_inv = np.copy(frame_b[::-1,::-1])

    piv = do_piv(frame_a, frame_b, True)
    piv_inv = do_piv(frame_a_inv, frame_b_inv, True)

    piv_noerror = do_piv(frame_a, frame_b, False)
    piv_inv_noerror = do_piv(frame_a_inv, frame_b_inv, False)

    u = piv.u
    ui = piv_inv.u[::-1, ::-1]

    u_noerror = piv_noerror.u
    ui_noerror = piv_inv_noerror.u[::-1, ::-1]

    u[np.isnan(u)] = 1000.
    ui[np.isnan(ui)] = -1000.

    u_noerror[np.isnan(u)] = 1000.
    ui_noerror[np.isnan(ui)] = -1000.

    f, (ax1, ax2) = plt.subplots(1, 2)
    f.canvas.set_window_title("Plot with outlier detection")
    ax1.imshow(u, interpolation='nearest')
    ax1.set_title("unrotated")
    ax2.imshow(-ui, interpolation='nearest')
    ax2.set_title("rotated")

    f, (ax1, ax2) = plt.subplots(1, 2)
    f.canvas.set_window_title("Plot without outlier detection")
    ax1.imshow(u_noerror, interpolation='nearest')
    ax1.set_title("unrotated")
    ax2.imshow(-ui_noerror, interpolation='nearest')
    ax2.set_title("rotated")

    print "difference with error: {}".format(np.sum(u+ui))
    print "difference without er: {}".format(np.sum(u_noerror+ui_noerror))

    plt.show()

def do_piv(frame_a, frame_b,outlier=True):
    """
    for finding the error use the boolean variable outlier
    to use or not use the outlier detection and replacement
    """

    #PIV1
    piv = pypiv.DirectPIV(frame_a, frame_b, window_size=32,
                            search_size=32, distance=16)
    piv.correlate_frames()
    if outlier:
        pypiv.filters.outlier_from_local_median(piv, 2.0)
        pypiv.filters.replace_outliers(piv)
    pypiv.filters.median_filter(piv)

    #PIV2
    piv = pypiv.AdaptivePIV(piv, window_size=32,
                                  search_size=32, distance=16)
    piv.correlate_frames()

    if outlier:
        pypiv.filters.outlier_from_local_median(piv, 2.0)
        pypiv.filters.replace_outliers(piv)
    pypiv.filters.median_filter(piv)

    #PIV3
    piv = pypiv.AdaptivePIV(piv, window_size=32,
                                  search_size=32, distance=8)
    piv.correlate_frames()
    if outlier:
        pypiv.filters.outlier_from_local_median(piv, 2.0)
        pypiv.filters.replace_outliers(piv)
    pypiv.filters.median_filter(piv)

    return piv


if __name__=='__main__':
    main()
