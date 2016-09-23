import pypiv
import matplotlib.pyplot as plt
from glob import glob

def main():
    imgs = glob('images/finger*')
    frames = [plt.imread(x) for x in imgs]

    frame_a = frames[0]
    frame_b = frames[1]


    piv = pypiv.DirectPIV(frame_a, frame_b, window_size=32,
                            search_size=32, distance=16, dt=1)

    u, v = piv.correlate_frames()
    plt.imshow(u)
    plt.show()


if __name__=='__main__':
    main()
