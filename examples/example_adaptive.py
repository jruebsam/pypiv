import pypiv
import numpy as np
import matplotlib.pyplot as plt
from glob import glob

def main():
    imgs = glob('images/finger*')
    frames = [plt.imread(x) for x in imgs]
    frame_a, frame_b = frames[0], frames[1]

    #PIV1
    piv = pypiv.DirectPIV(frame_a, frame_b, window_size=32,
                            search_size=32, distance=16, dt=1)
    piv.correlate_frames()
    mask = pypiv.filters.local_median_filter(piv.u, piv.v)
    mask += np.isnan(piv.u) + np.isnan(piv.v)
    piv.u, piv.v = pypiv.filters.replace_outliers(piv.u, piv.v, mask)
    piv.u = pypiv.filters.median_filter(piv.u, 2)
    piv.v = pypiv.filters.median_filter(piv.v, 2)


    #PIV2
    piv = pypiv.AdaptivePIV(piv, window_size=32,
                                  search_size=32, distance=16)
    piv.correlate_frames()
    mask = pypiv.filters.local_median_filter(piv.u, piv.v)
    mask += np.isnan(piv.u) + np.isnan(piv.v)
    piv.u, piv.v = pypiv.filters.replace_outliers(piv.u, piv.v, mask)
    piv.u = pypiv.filters.median_filter(piv.u, 2)
    piv.v = pypiv.filters.median_filter(piv.v, 2)

    #PIV3
    piv = pypiv.AdaptivePIV(piv, window_size=32,
                                  search_size=32, distance=8)
    u, v = piv.correlate_frames()
    mask = pypiv.filters.local_median_filter(piv.u, piv.v)
    mask += np.isnan(piv.u) + np.isnan(piv.v)
    piv.u, piv.v = pypiv.filters.replace_outliers(piv.u, piv.v, mask)
    piv.u = pypiv.filters.median_filter(piv.u, 2)
    piv.v = pypiv.filters.median_filter(piv.v, 2)
    #OUTPUT
    plt.imshow(u)
    plt.show()


if __name__=='__main__':
    main()
