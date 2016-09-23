import pypiv
import numpy as np
import matplotlib.pyplot as plt
from glob import glob

def main():
    imgs = ['images/finger1.png', 'images/finger2.png']
    frames = [plt.imread(x) for x in imgs]
    frame_a, frame_b = frames[0], frames[1]

    #PIV1
    piv = pypiv.DirectPIV(frame_a, frame_b, window_size=32,
                            search_size=32, distance=16)
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
    x, y, u, v = pypiv.postprocess.compute_coordinate_transformations(piv)
    plt.imshow(v.T, origin='lower', extent=[np.min(x), np.max(x), np.min(y), np.max(y)])
    plt.show()


if __name__=='__main__':
    main()
