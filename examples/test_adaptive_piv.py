import matplotlib as mt
backend = mt.get_backend()
if backend == 'agg':
	mt.use('TKagg')
import pypiv
import matplotlib.pyplot as plt
from glob import glob

def main():
    imgs = glob('images/real_ana_finger*')
    frames = [plt.imread(x) for x in imgs]

    frame_a = frames[0]
    frame_b = frames[1]

    piv = pypiv.DirectPIV(frame_a, frame_b, window_size=32,
                            search_size=32, distance=16)
    u, v = piv.correlate_frames()

    adapt_piv = pypiv.AdaptivePIV(piv, window_size=32,
                                  search_size=32, distance=16,
                                  ipmethod='cubic')
    u, v = adapt_piv.correlate_frames()

    adapt_piv = pypiv.AdaptivePIV(piv, window_size=32,
                                  search_size=32, distance=8,
                                  ipmethod='cubic')
    u, v = adapt_piv.correlate_frames()

    plt.imshow(u)
    plt.clim(-5, 5)
    plt.show()


if __name__=='__main__':
    main()
