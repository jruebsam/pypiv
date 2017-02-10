import numpy as np
from scipy.stats import linregress as li
from math import exp

def calc_factor(field,stepsize=0.01):
    result_pos = []
    result_neg = []
    outlier = 1.
    alpha = 0.
    while alpha <= np.max(field)+stepsize:
        pos = alpha
        neg = 0.
        filtered = np.copy(field)
        filtered[filtered<=neg] = np.nan
        filtered[filtered>pos] = np.nan
        outlier = np.count_nonzero(~np.isnan(filtered))/np.float(np.count_nonzero(~np.isnan(field)))
        result_pos.append([alpha,outlier])
        alpha += stepsize
    outlier = 1.
    alpha = 0.
    while alpha <= np.abs(np.min(field))+stepsize:
        pos = 0.
        neg = -1.*alpha
        filtered = np.copy(field)
        filtered[filtered<=neg] = np.nan
        filtered[filtered>pos] = np.nan
        outlier = np.count_nonzero(~np.isnan(filtered))/np.float(np.count_nonzero(~np.isnan(field)))
        result_neg.append([-1.*alpha,outlier])
        alpha += stepsize

    return (np.array(result_pos),np.array(result_neg))

def filter(u,v,tfactor=3.):
    up = np.copy(u)
    up[up<=0.] = 0.
    un = np.copy(u)
    un[un>0.] = 0.

    vp = np.copy(v)
    vp[vp<=0.] = 0.
    vn = np.copy(v)
    vn[vn>0.] = 0.

    numberup = np.count_nonzero(up)/np.float(np.count_nonzero(u))
    numberun = np.count_nonzero(un)/np.float(np.count_nonzero(u))
    numbervp = np.count_nonzero(vp)/np.float(np.count_nonzero(v))
    numbervn = np.count_nonzero(vn)/np.float(np.count_nonzero(v))

    #get alpha dependency
    dalpha = .01
    up_alpha, un_alpha = calc_factor(u,dalpha)
    vp_alpha, vn_alpha = calc_factor(v,dalpha)

    dup_alpha = np.gradient(up_alpha[:,1],dalpha)
    dun_alpha = np.gradient(un_alpha[:,1],dalpha)
    dvp_alpha = np.gradient(vp_alpha[:,1],dalpha)
    dvn_alpha = np.gradient(vn_alpha[:,1],dalpha)

    #get boundaries
    boundup = np.sum(dup_alpha[0:5])/5./np.exp(tfactor)
    boundun = np.sum(dun_alpha[0:5])/5./np.exp(tfactor)
    boundvp = np.sum(dvp_alpha[0:5])/5./np.exp(tfactor)
    boundvn = np.sum(dvn_alpha[0:5])/5./np.exp(tfactor)

    #get indizes and exponential
    indexup = np.where(dup_alpha<boundup)
    indexun = np.where(dun_alpha<boundun)
    indexvp = np.where(dvp_alpha<boundvp)
    indexvn = np.where(dvn_alpha<boundvn)
    cut_up = np.int(np.sum(indexup[0][0:5])/5.)
    cut_un = np.int(np.sum(indexun[0][0:5])/5.)
    cut_vp = np.int(np.sum(indexvp[0][0:5])/5.)
    cut_vn = np.int(np.sum(indexvn[0][0:5])/5.)
    nup = np.polyfit(np.log( up_alpha[1:cut_up,0]),np.log(up_alpha[1:cut_up,1]),1)
    nun = np.polyfit(np.log(-un_alpha[1:cut_un,0]),np.log(un_alpha[1:cut_un,1]),1)
    nvp = np.polyfit(np.log( vp_alpha[1:cut_vp,0]),np.log(vp_alpha[1:cut_vp,1]),1)
    nvn = np.polyfit(np.log(-vn_alpha[1:cut_vn,0]),np.log(vn_alpha[1:cut_vn,1]),1)
    upos =  exp(-nup[1]/nup[0])
    uneg = -exp(-nun[1]/nun[0])
    vpos =  exp(-nvp[1]/nvp[0])
    vneg = -exp(-nvn[1]/nvn[0])

    #filter + clamping
    if upos > np.max(up):
        upos = np.max(up)
    if uneg < np.min(un):
        uneg = np.min(un)
    if vpos > np.max(vp):
        vpos = np.max(vp)
    if vneg < np.min(vn):
        vneg = np.min(vn)
    upos *= (0.5+numberup)
    uneg *= (0.5+numberun)
    vpos *= (0.5+numbervp)
    vneg *= (0.5+numbervn)
    print "u-+= ",uneg,upos
    print "v-+= ",vneg,vpos
    uvf = np.copy(u)
    uvf[uvf<uneg] = np.nan
    uvf[uvf>upos] = np.nan

    vvf = np.copy(v)
    vvf[vvf<vneg] = np.nan
    vvf[vvf>vpos] = np.nan

    return uvf,vvf

