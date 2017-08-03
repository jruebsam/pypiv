import numpy as np
from scipy.stats import linregress as li
from math import exp

def calc_factor(field,stepsize=0.01):
    """
    Function for calculation of the summed binning.

    The returned result is an integral over the binning of the velocities.
    It is done for the negative and positive half separately.

    :param field: is a 1D field which will be binned
    :param stepsize: is the step size for the velocity
    :return (positive,negative): 
        velocities and the binning result for positive half and negative half are returned
        as a tuple of numpy arrays
    """
    result_pos = []
    result_neg = []
    alpha = 0.
    #: binning of the positive half
    while alpha <= np.max(field)+stepsize:
        pos = alpha
        neg = 0.
        filtered = np.copy(field)
        filtered[filtered<=neg] = np.nan
        filtered[filtered>pos] = np.nan
        outlier = np.count_nonzero(~np.isnan(filtered))/np.float(np.count_nonzero(~np.isnan(field)))
        result_pos.append([alpha,outlier])
        alpha += stepsize
    alpha = 0.
    #: binning of the negative half
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

def calc_derivative(field,stepsize=0.01):
    """
    Function for calculation of the binning.

    The returned result is the binning of the velocities.
    It is called derivative because it is mathematically the derivative of the function:

    .. function:: velofilter.calc_factor

    It is done for the negative and positive half separately.

    :param field:  is a 1D field which will be binned
    :param stepsize:  is the step size for the velocity
    :return (positive,negative): 
        velocities and the binning result for positive half and negative half are returned
        as a tuple
    """
    result_pos = []
    result_neg = []
    outlier = 1.
    alpha = 0.
    while alpha <= np.max(field)+stepsize:
        pos = alpha+stepsize
        neg = alpha
        filtered = np.copy(field)
        filtered[(filtered<=neg) | (filtered>pos)] = np.nan
        #filtered[filtered>pos] = np.nan
        outlier = np.count_nonzero(~np.isnan(filtered))/np.float(np.count_nonzero(~np.isnan(field)))
        result_pos.append([alpha,outlier])
        alpha += stepsize
    outlier = 1.
    alpha = 0.
    while alpha <= np.abs(np.min(field))+stepsize:
        pos = -1.*alpha
        neg = -1.*(alpha+stepsize)
        filtered = np.copy(field)
        filtered[(filtered<=neg) | (filtered>pos)] = np.nan
        #filtered[filtered>pos] = np.nan
        outlier = np.count_nonzero(~np.isnan(filtered))/np.float(np.count_nonzero(~np.isnan(field)))
        result_neg.append([-1.*alpha,outlier])
        alpha += stepsize

    return (np.array(result_pos),np.array(result_neg))

def filter(piv,tfactor=3.,dalpha=.01):
    """
    Function for calculating the cutoff values.

    :param object piv: PIV class object

        This is supposed to be an object from a Direct or adaptive Class
        it is needed to get the velocities
    :param double tfactor: Factor for cutoff in the velocity binning

        The default value is set to 3 which works for many cases
    :param double dalpha: value for differential velocity

        The default is set to .01 which work for many cases
        if the velocities vary over a larger ranger use a larger value
    """

    #: pre sampling
    numberup = np.count_nonzero(piv.u<=0.)/np.float(np.count_nonzero(piv.u))
    numberun = np.count_nonzero(piv.u>0.)/np.float(np.count_nonzero(piv.u))
    numbervp = np.count_nonzero(piv.v<=0.)/np.float(np.count_nonzero(piv.v))
    numbervn = np.count_nonzero(piv.v>0.)/np.float(np.count_nonzero(piv.v))
    upos = numberup 
    uneg = numberun
    vpos = numbervp 
    vneg = numbervn

    #: get alpha dependency
    up_alpha, un_alpha = calc_factor(piv.u,dalpha)
    vp_alpha, vn_alpha = calc_factor(piv.v,dalpha)

    #: calculate derivative directly from data
    dup_alpha1, dun_alpha1 = calc_derivative(piv.u,dalpha)
    dvp_alpha1, dvn_alpha1 = calc_derivative(piv.v,dalpha)

    dup_alpha = dup_alpha1[:,1]
    dun_alpha = dun_alpha1[:,1]
    dvp_alpha = dvp_alpha1[:,1]
    dvn_alpha = dvn_alpha1[:,1]

    #get boundaries
    boundup = np.sum(dup_alpha[0:5])/5./np.exp(tfactor)
    boundun = np.sum(dun_alpha[0:5])/5./np.exp(tfactor)
    boundvp = np.sum(dvp_alpha[0:5])/5./np.exp(tfactor)
    boundvn = np.sum(dvn_alpha[0:5])/5./np.exp(tfactor)

    #get indices and exponential
    if upos != 0.:
        indexup = np.where(dup_alpha<boundup)
        cut_up = np.int(np.sum(indexup[0][0:5])/5.)
        nup = np.polyfit(np.log( up_alpha[1:cut_up,0]),np.log(up_alpha[1:cut_up,1]),1)
        upos =  exp(-nup[1]/nup[0])
    if uneg != 0.:
        indexun = np.where(dun_alpha<boundun)
        cut_un = np.int(np.sum(indexun[0][0:5])/5.)
        nun = np.polyfit(np.log(-un_alpha[1:cut_un,0]),np.log(un_alpha[1:cut_un,1]),1)
        uneg = -exp(-nun[1]/nun[0])
    if vpos != 0.:
        indexvp = np.where(dvp_alpha<boundvp)
        cut_vp = np.int(np.sum(indexvp[0][0:5])/5.)
        nvp = np.polyfit(np.log( vp_alpha[1:cut_vp,0]),np.log(vp_alpha[1:cut_vp,1]),1)
        vpos =  exp(-nvp[1]/nvp[0])
    if vneg != 0.:
        indexvn = np.where(dvn_alpha<boundvn)
        cut_vn = np.int(np.sum(indexvn[0][0:5])/5.)
        nvn = np.polyfit(np.log(-vn_alpha[1:cut_vn,0]),np.log(vn_alpha[1:cut_vn,1]),1)
        vneg = -exp(-nvn[1]/nvn[0])

    #filter + clamping
    if upos > np.max(piv.u):
        upos = np.max(piv.u)
    if uneg < np.min(piv.u):
        uneg = np.min(piv.u)
    if vpos > np.max(piv.v):
        vpos = np.max(piv.v)
    if vneg < np.min(piv.v):
        vneg = np.min(piv.v)

    #equalizing the cutoff
    upos *= (0.5+numberup)
    uneg *= (0.5+numberun)
    vpos *= (0.5+numbervp)
    vneg *= (0.5+numbervn)

    #making the mask
    masku = (piv.u<uneg) | (piv.u>upos)
    maskv = (piv.v<vneg) | (piv.v>vpos)
    piv.u[masku] = np.nan
    piv.v[maskv] = np.nan

