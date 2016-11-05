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

    piv = do_piv(frame_a, frame_b)
    piv_inv = do_piv(frame_a_inv, frame_b_inv)


    u = piv.u
    ui = piv_inv.u[::-1, ::-1]

    u[np.isnan(u)] = 1000.
    ui[np.isnan(ui)] = -1000.

    f, (ax1, ax2) = plt.subplots(1, 2)
    ax1.imshow(u, interpolation='nearest')
    ax2.imshow(-ui, interpolation='nearest')

    print np.sum(u+ui)

    plt.show()

def do_piv(frame_a, frame_b):

    #PIV1
    piv = pypiv.DirectPIV(frame_a, frame_b, window_size=32,
                            search_size=32, distance=16)
    piv.correlate_frames()
    #pypiv.filters.outlier_from_local_median(piv, 2.0)
    #pypiv.filters.replace_outliers(piv)
    pypiv.filters.median_filter(piv)

    #PIV2
    piv = pypiv.AdaptivePIV(piv, window_size=32,
                                  search_size=32, distance=16)
    piv.correlate_frames()

    #pypiv.filters.outlier_from_local_median(piv, 2.0)
    #pypiv.filters.replace_outliers(piv)
    pypiv.filters.median_filter(piv)

    #PIV3
    piv = pypiv.AdaptivePIV(piv, window_size=32,
                                  search_size=32, distance=8)
    piv.correlate_frames()
    #pypiv.filters.outlier_from_local_median(piv, 2.0)
    #pypiv.filters.replace_outliers(piv)
    pypiv.filters.median_filter(piv)

    return piv


if __name__=='__main__':
    main()
