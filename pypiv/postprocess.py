import numpy as np

def compute_coordinate_transformations(piv, width=100, dt=1.):
    ''''
    Compute Coordinate system  transformation from
          ------ y              y
         |                      |
         |             to       |
         x                       ------ x

    with x  ->  -y , u -> v , y -> x, v -> -u
    and time scaling
    '''

    ly, lx = piv.frame_a.shape
    window_size = piv._interogation_ws
    distance = piv._distance

    nx = (lx - window_size)//distance+1
    ny = (ly - window_size)//distance+1

    x = np.arange(0, nx*distance, distance) + window_size/2
    y = np.arange(0, ny*distance, distance) + window_size/2

    X, Y = np.meshgrid(x, y)
    X, Y = X/float(lx)*width, Y/float(ly)*width

    U, V = piv.v.T/dt, -piv.u.T/dt
    return X, Y, U, V

