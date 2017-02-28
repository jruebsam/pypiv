import numpy as np
import matplotlib.pyplot as plt

from pypiv import FFTCorrelator
from scipy.special import erf

x, y = np.mgrid[0:128, 0:128]
#def particle(x0, y0, d):
#    return np.exp(-((x - x0)**2 + (y - y0)**2)/(0.42*d)**2)

def particle(x0, y0, d):
    sigma = 0.42*d
    C = np.pi/8.*sigma**2
    out  = (erf((x - x0 + 0.5)/(sigma*np.sqrt(2))) - erf((x - x0 - 0.5)/(sigma*np.sqrt(2))))
    out *= (erf((y - y0 + 0.5)/(sigma*np.sqrt(2))) - erf((y - y0 - 0.5)/(sigma*np.sqrt(2))))
    return C*out

def main():
    N = 10
    for method in ['gaussian', '9point', 'parabolic']:
        err = []
        d = []
        diameters = np.linspace(1, 15., 101.)
        for dia in diameters:
            frame1 =  particle(64, 64, dia)
            for i in range(N):
                shiftx = 10 + np.random.rand()
                shifty = 10 + np.random.rand()
                frame2 =  particle(64+shiftx, 64+shifty, dia)

                corr = FFTCorrelator(128, 128)
                xn, yn = corr.get_displacement(frame1, frame2, method)
                error = np.sqrt((xn - shiftx)**2 + (yn - shifty)**2)
                err.append(error)
                d.append(dia)

        plt.scatter(d, err, label=method)
    plt.legend()
    plt.show()


if __name__=='__main__':
    main()
