import numpy as np
import numpy.linalg as nl

def find_peak(corr, method='gaussian'):
    i, j = np.unravel_index(corr.argmax(), corr.shape)
    if check_peak_position(corr, i, j) is False:
        return np.nan, np.nan
    window = corr[i-1:i+2, j-1:j+2]

    if method == 'gaussian':
        subpixel_interpolation = gaussian
    elif method == 'centroid':
        subpixel_interpolation = centroid
    elif method == 'parabolic':
        subpixel_interpolation = parabolic
    elif method == '9point':
        subpixel_interpolation = gaussian2D
    else:
        raise Exception('Sub pixel interpolation method not found!')
    try:
        dx, dy = subpixel_interpolation(window)
    except:
        return np.nan, np.nan
    else:
        return (i + dx, j + dy)

def check_peak_position(corr, i, j):
    dist = 3
    li, lj = corr.shape
    i_inside = (i >= dist) & (i < li - dist)
    j_inside = (j >= dist) & (j < lj - dist)
    if i_inside and j_inside:
        return True
    else:
        return False

def gaussian(window):
    ip  = lambda x : (np.log(x[0]) - np.log(x[2]))\
                    /(2*np.log(x[2]) - 4*np.log(x[1]) + 2*np.log(x[0]))
    return ip(window[:, 1]), ip(window[1])

def centroid(window):
    ip = lambda x : (x[2] - x[0])/(x[0] + x[1] + x[2])
    return ip(window[:, 1]), ip(window[1])

def parabolic(window):
    ip = lambda x : (x[0] - x[2])/(2*x[0] - 4*x[1] + 2*x[2])
    return ip(window[:, 1]), ip(window[1])

def gaussian2D(window):
    w = np.ones((3, 3))*(1./9)
    rhs = np.zeros(6)
    M = np.zeros((6,6))
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            rhs = rhs     +     np.array([i*w[i+1, j+1]*np.log(np.abs(window[i+1, j+1])),
                                          j*w[i+1, j+1]*np.log(np.abs(window[i+1, j+1])),
                                        i*j*w[i+1, j+1]*np.log(np.abs(window[i+1, j+1])),
                                        i*i*w[i+1, j+1]*np.log(np.abs(window[i+1, j+1])),
                                        j*j*w[i+1, j+1]*np.log(np.abs(window[i+1, j+1])),
                                            w[i+1, j+1]*np.log(np.abs(window[i+1, j+1]))], dtype='float')

            M = M + w[i+1, j+1]*np.array([[  i*i,   i*j,   i*i*j,   i*i*i,   i*j*j,   i],
                                          [  i*j,   j*j,   i*j*j,   i*i*j,   j*j*j,   j],
                                          [i*i*j, i*j*j, i*i*j*j, i*i*i*j, i*j*j*j, i*j],
                                          [i*i*i, i*i*j, i*i*i*j, i*i*i*i, i*i*j*j, i*i],
                                          [i*j*j, j*j*j, i*j*j*j, i*i*j*j, j*j*j*j, j*j],
                                          [    i,     j,     i*j,     i*i,     j*j,   1]], dtype='float')
    solution = nl.solve(M, rhs)

    dx = (    solution[2]*solution[1] - 2.0*solution[0]*solution[4])/ \
         (4.0*solution[3]*solution[4] -     solution[2]*solution[2])

    dy = (    solution[2]*solution[0] - 2.0*solution[1]*solution[3])/ \
         (4.0*solution[3]*solution[4] -     solution[2]*solution[2])

    return dx, dy


