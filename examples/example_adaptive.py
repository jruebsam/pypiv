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
    pypiv.filters.outlier_from_local_median(piv, 2.0)
    pypiv.filters.replace_outliers(piv)
    pypiv.filters.median_filter(piv)


    #PIV2
    piv = pypiv.AdaptivePIV(piv, window_size=32,
                                  search_size=32, distance=16)
    piv.correlate_frames()
    pypiv.filters.outlier_from_local_median(piv, 2.0)
    pypiv.filters.replace_outliers(piv)
    pypiv.filters.median_filter(piv)

    #PIV3
    piv = pypiv.AdaptivePIV(piv, window_size=32,
                                  search_size=32, distance=8)
    piv.correlate_frames()
    pypiv.filters.outlier_from_local_median(piv, 2.0)
    pypiv.filters.replace_outliers(piv)
    pypiv.filters.median_filter(piv)

    #OUTPUT
    plt.imshow(piv.u)
    plt.show()


if __name__=='__main__':
    main()
