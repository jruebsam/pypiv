import numpy as np
import matplotlib.pyplot as plt

from pypiv import FFTCorrelator
from scipy.special import erf

x, y = np.mgrid[0:32, 0:32]
#def particle(x0, y0, d):
#    return np.exp(-((x - x0)**2 + (y - y0)**2)/(0.42*d)**2)

def particle(x0, y0, d):
    sigma = 0.42*d
    C = np.pi/8.*sigma**2
    out  = (erf((x - x0 + 0.5)/(sigma*np.sqrt(2))) - erf((x - x0 - 0.5)/(sigma*np.sqrt(2))))
    out *= (erf((y - y0 + 0.5)/(sigma*np.sqrt(2))) - erf((y - y0 - 0.5)/(sigma*np.sqrt(2))))
    return C*out

def main():
    N = 100
    f, (ax1,ax2) = plt.subplots(1,2)
    ax1.set_yscale("log", nonposy='clip')
    ax2.set_yscale("log", nonposy='clip')
    for method, color in zip(['9point', 'gaussian', 'parabolic', 'centroid'],['k*-','ro-','c+-', 'g.-']):
        err = []
        err_mean = []
        err_std = []
        d = []
        diameters = np.linspace(1, 15, 101)
        print method
        for dia in diameters:
            frame1 =  particle(16, 16, dia)
            error_n = []
            for i in range(N):
                shiftx = 10 + np.random.rand()
                shifty = 10 +np.random.rand()
                frame2 =  particle(16+shiftx, 16+shifty, dia)

                corr = FFTCorrelator(32, 32)
                xn, yn = corr.get_displacement(frame1, frame2, method)
                error = np.sqrt((xn - shiftx)**2 + (yn - shifty)**2)
                error_n.append(error)
            err.append(np.max(error_n))
            err_mean.append(np.mean(error_n))
            err_std.append(np.std(error_n))
            d.append(dia)

        ax1.semilogy(d, err, color, label=method)
        ax2.errorbar(d, err_mean, yerr=err_std, fmt=color, label=method)
    ax1.set_xlabel("diameter [pixel]")
    ax1.set_ylabel("shift error [pixel]")
    ax1.set_title("maximum error")
    ax2.set_xlabel("diameter [pixel]")
    ax2.set_ylabel("shift error [pixel]")
    ax2.set_title("mean error")
    ax1.grid(True, which="both")
    ax2.grid(True, which="both")
    ax1.legend()
    ax2.legend()
    f.tight_layout()
    plt.show()


if __name__=='__main__':
    main()
