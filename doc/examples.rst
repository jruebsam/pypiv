Example Tutorial
================





Single PIV evaluation
---------------------

Adaptive Piv with multiple steps
--------------------------------

.. code-block:: python

    import pypiv
    import numpy as np
    import matplotlib.pyplot as plt
    from glob import glob

    imgs = ['images/finger1.png', 'images/finger2.png']
    #imgs = ['images/test1.png', 'images/test2.png']
    frames = [plt.imread(x) for x in imgs]
    frame_a, frame_b = frames[0], frames[1]

.. code-block:: python

    piv = pypiv.DirectPIV(frame_a, frame_b, window_size=32,
                            search_size=32, distance=16)
    piv.correlate_frames()
    pypiv.filters.outlier_from_local_median(piv, 2.0)
    pypiv.filters.replace_outliers(piv)
    pypiv.filters.median_filter(piv)

.. code-block:: python

    piv = pypiv.AdaptivePIV(piv, window_size=32,
                                  search_size=32, distance=16, ipmethod='cubic')
    piv.correlate_frames()
    pypiv.filters.outlier_from_local_median(piv, 2.0)
    pypiv.filters.replace_outliers(piv)
    pypiv.filters.median_filter(piv)

.. code-block:: python

    piv = pypiv.AdaptivePIV(piv, window_size=32,
                                  search_size=32, distance=8, ipmethod='cubic')#, deformation='central')
    piv.correlate_frames()
    pypiv.filters.outlier_from_local_median(piv, 2.0)
    pypiv.filters.replace_outliers(piv)
    pypiv.filters.median_filter(piv)

.. code-block:: python

    x, y, u, v = pypiv.postprocess.compute_coordinate_transformations(piv)

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.quiver(x,y,u.T,v.T)

    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    cax2 = ax2.imshow(v.T, origin='lower')
    fig2.colorbar(cax2)

    fig3 = plt.figure()
    ax3 = fig3.add_subplot(111)
    cax3 = ax3.imshow(u.T, origin='lower')
    fig3.colorbar(cax3)
    plt.show()


