import matplotlib as mt
mt.use('TKAGG')
import pypiv
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from scipy.ndimage.interpolation import zoom

def main():
    imgs = ['images/real_ana_finger_0.tif', 'images/real_ana_finger_1.tif']
    #imgs = ['images/real_fingers-0.bmp', 'images/real_fingers-1.bmp']
    frames = [plt.imread(x) for x in imgs]
    frame_a, frame_b = frames[0], frames[1]
    #frame_a = zoom(frame_a,2)
    #frame_b = zoom(frame_b,2)

    #PIV1
    piv = pypiv.DirectPIV(frame_a, frame_b, window_size=32,
                            search_size=32, distance=16)
    piv.correlate_frames()
    pypiv.filters.outlier_from_local_median(piv, 2.0)
    pypiv.filters.replace_outliers(piv)
    pypiv.filters.median_filter(piv)

    #PIV2
    piv = pypiv.AdaptivePIV(piv, window_size=32,
                                  search_size=32, distance=16, ipmethod='bilinear')
    piv.correlate_frames()
    pypiv.filters.outlier_from_local_median(piv, 2.0)
    pypiv.filters.replace_outliers(piv)
    pypiv.filters.median_filter(piv)

    #PIV3
    piv = pypiv.AdaptivePIV(piv, window_size=32,
                                  search_size=32, distance=8, ipmethod='bilinear')
    piv.correlate_frames()
    pypiv.filters.replace_outliers(piv)

    resu = pypiv.velofilter.filter(piv,tfactor=0.5,demo=True)
    print("pos")
    print(resu[4])
    print(resu[0])
    print(resu[1])
    print(resu[2])
    print(resu[3])
    print("index")
    print(resu[10])
    print("bounds")
    print(resu[5])
    print("cut")
    print(resu[6])
    print("fit")
    print(resu[7])

    #pypiv.filters.outlier_from_local_median(piv, 2.0)
    #pypiv.filters.replace_outliers(piv)
    #pypiv.filters.median_filter(piv)

    #OUTPUT
    x, y, u, v = pypiv.postprocess.compute_coordinate_transformations(piv)

    #Velofilter behaviour
    labels      = ["up","un","vp","vn"]
    fig4,ax4    = plt.subplots(2,2)
    for i in range(2):
        for j in range(2):
            ind = int(i*2+j)
            ax4[i,j].loglog(np.abs(resu[8][ind][1:,0]),
                            resu[8][ind][1:,1],"r-")
            ax4[i,j].loglog(np.abs(resu[8][ind][1:,0]),
                            np.exp(resu[7][ind][1])*np.abs(resu[8][ind][1:,0])**resu[7][ind][0]
                            ,"b-")
            ax4[i,j].set_ylabel(labels[ind])
            ax4[i,j].set_xlabel("alpha")
            ax4[i,j].set_ylim([6e-2,1])
            ax4[i,j].axvline(np.abs(resu[2][ind]),color="b")
            ax4[i,j].axhline(1,color="r")
            ax4[i,j].axvline(np.abs(resu[3][ind]),color="k")

    labels      = ["dup","dun","dvp","dvn"]
    fig5,ax5    = plt.subplots(2,2)
    for i in range(2):
        for j in range(2):
            ax5[i,j].plot(  resu[9][int(i*2+j)][:,0],
                            resu[9][int(i*2+j)][:,1],"r-")
            ax5[i,j].set_ylabel(labels[int(i*2+j)])
            ax5[i,j].set_xlabel("alpha")

    labels      = ["dup","dun","dvp","dvn"]
    fig6,ax6    = plt.subplots(2,1)
    masku       = ~np.isnan(u.flatten())
    maskv       = ~np.isnan(v.flatten())
    ax6[0].hist(u.flatten()[masku],bins=200)
    ax6[1].hist(v.flatten()[maskv],bins=200)
    ax6[0].set_ylabel("u")
    ax6[1].set_ylabel("v")

    #Piv results
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


if __name__=='__main__':
    main()
