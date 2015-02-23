#!/usr/bin/python
"""
use various scipy.optimize algorithms to fit Gaussian in uv space

Should be very simple, described only by amplitude and sigma

leastsq example here:
http://docs.scipy.org/doc/scipy/reference/tutorial/optimize-1.py
"""
import os
from math import degrees, e
from operator import itemgetter
from power_law import power_law, power_law_curvature, rsq
from scipy.optimize import leastsq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np

#REF_FREQ=150.
REF_FREQ=408.


INDIR       = '.'
INFILENAME  = 'marco.csv'
OUTDIR      = '.'
OUTFILENAME = 'marco_fits_408.csv'
DOPLOT      = False

outfile = open(OUTFILENAME, 'w')
def fit_line(x, y, y_err):
    """
    fit straight line and determine errors on fit *based on y_err alone*
    x, y and y_err are all identical-length 1D arrays

    returns m, c, m_error, c_error
    where m_error and c_error are the absolute 1-sigma errors on the slope
    and intercept respectively

    >>> fit_line(array([0,1,2]), array([0,1,2]), array([1, 1, 1]))
    (1.0, 0.0, 0.70710678118654724, 0.91287092917527646, 0.0)
    fit_line(array([0,1,2]), array([1,2,3]), array([1, 1, 1]))

    """
    # define our (line) fitting function
    fitfunc = lambda p, x: p[0] + p[1] * (x)
    errfunc = lambda p, x, y, y_err: (y - fitfunc(p, x)) / y_err

    pinit = [1.0, -1.0]
    out = leastsq(errfunc, pinit,
          args=(x, y, y_err), full_output=1)

    pfinal = out[0]
    covar = out[1]

    m = pfinal[1]
    c = pfinal[0]

    if not covar is None:
        m_err = np.sqrt(covar[1][1])
        c_err = np.sqrt(covar[0][0])
    else:
        # degenerate case where all y are equal
        # FIXME do this properly!
        m_err = np.nan
        c_err = np.nan

    # measure of goodness of fit.
    if len(x) > 2:
        me1 = np.sqrt(sum(errfunc(pfinal, x, y, y_err)**2)/(len(x)-2))
    else:
        me1 = np.nan

    return m, c, m_err, c_err, me1

def fit_curvature(x, y, y_err):
    """
    fit straight line and determine errors on fit *based on y_err alone*
    x, y and y_err are all identical-length 1D arrays

    returns a2, a1, a0, a2_err, a1_err, a0_err
    where m_error and c_error are the absolute 1-sigma errors on the slope
    and intercept respectively

    """
    # define our (line) fitting function
    fitfunc = lambda p, x: p[0] + (p[1] * x) + (p[2] * x**2)
    errfunc = lambda p, x, y, y_err: (y - fitfunc(p, x)) / y_err

    pinit = [1.0, -1.0, 0.0]
    out = leastsq(errfunc, pinit,
          args=(x, y, y_err), full_output=1)

    pfinal = out[0]
    covar = out[1]

    a0 = pfinal[0]
    a1 = pfinal[1]
    a2 = pfinal[2]

    if not covar is None:
        a0_err = np.sqrt(covar[0][0])
        a1_err = np.sqrt(covar[1][1])
        a2_err = np.sqrt(covar[2][2])
    else:
        # degenerate case where all y are equal
        # FIXME do this properly!
        a0_err = np.nan
        a1_err = np.nan
        a2_err = np.nan

    # measure of goodness of fit.
    if len(x) > 3:
        me1 = np.sqrt(sum(errfunc(pfinal, x, y, y_err)**2)/(len(x)-3))
    else:
        me1 = np.nan

    return a2, a1, a0, a2_err, a1_err, a0_err, me1


flux_cols =     ["S_vlss",
                 "S_culgoora80",
                 "S_culgoora160",
                 "S_mwacs",
                 "S_wsrt",
                 "S_mrc",
                 "S_sumss_north",
                 "S"]

flux_error_cols = ["e_S_vlss",
                   "e_S_culgoora80",
                   "e_S_culgoora160",
                   "e_S_mwacs",
                   "e_S_wsrt",
                   "e_S_mrc",
                   "e_S_sumss_north",
                   "e_S"]

usecols = ["ID", "primary", "secondary"] + flux_cols + flux_error_cols

marco = np.genfromtxt("marco.csv", delimiter=',', names=True, usecols=usecols, dtype=None)

i=0

print >> outfile, "ID,S_408_1,e_S408_1,SpIndex_1,e_SpIndex_1,me1_1,S_408_2,e_S408_2,SpIndex_2,e_SpIndex_2,Curvature_2,e_Curvature_2,me1_2"

for c, cat in enumerate((np.compress(marco["primary"] == "nvss", marco), np.compress(marco["primary"] == "sumss_south", marco))):
    if c == 0:
        NAMES = np.array(("vlss", "culgoora80", "culgoora160", "mwacs", "wsrt", "mrc", "sumss", "nvss"))
        FREQS = np.array((74., 80., 160., 180., 326., 408., 843., 1400.))
    if c == 1:
        NAMES = np.array(("vlss", "culgoora80", "culgoora160", "mwacs", "wsrt", "mrc", "sumss_north", "sumss_south"))
        FREQS = np.array((74., 80., 180., 160., 326., 408., 843., 843.))
    for source_id, fluxes, flux_errors in zip(cat["ID"], cat[flux_cols].view((np.float64, len(flux_cols))), cat[flux_error_cols].view((np.float64, len(flux_cols)))):

        print source_id,
        #filter out NaNs
        nn = ~np.isnan(fluxes)
        fluxes =           fluxes[nn]
        flux_errors = flux_errors[nn]
        freqs =             FREQS[nn]
        names =             NAMES[nn]
        flux_errors = np.where(flux_errors == 0, fluxes/100., flux_errors)

        if len(fluxes) > 1:
            alpha1, flux_ref1, alpha1_err, flux_ref1_err, me1_1 = fit_line(np.log10(freqs/REF_FREQ), np.log10(fluxes), np.log(10)**-1 * flux_errors / fluxes)
            flux_ref1 = 10**flux_ref1
            flux_ref1_err = np.log10(e)**-1*flux_ref1*flux_ref1_err
        else:
            print "Warning, source with only one flux measurement!"
            continue
        print

        if len(fluxes) > 2:
            curvature = True
            phi, alpha, flux_ref, phi_err, alpha_err, flux_ref_err, me1 = fit_curvature(np.log10(freqs/REF_FREQ), np.log10(fluxes), np.log(10)**-1 * flux_errors / fluxes)
            flux_ref = 10**flux_ref
            flux_ref_err = np.log10(e)**-1*flux_ref1*flux_ref_err
        else:
            curvature = False
            phi, alpha, flux_ref, phi_err, alpha_err, flux_ref_err, me1 = (np.nan,)*7
        i+=1
        print >> outfile, '"%s",' % source_id + ",".join(["%e" % i for i in (flux_ref1, flux_ref1_err, alpha1, alpha1_err,me1_1, flux_ref, flux_ref_err, alpha, alpha_err, phi, phi_err, me1)])
        #if i % 100 == 0:
            #print i

#        #jackknife
#        jn = []
#        f  = log10(array(CAT_FREQS)/REF_FREQ)
#        s  = log10(array(cat_fluxes))
#        er = log(10)**-1 * cat_flux_errs / cat_fluxes
#        for i in range(len(CAT_FREQS)):
#            jnf = array([j for k, j in enumerate(f)  if not k == i])
#            jns = array([j for k, j in enumerate(s) if not k == i])
#            jne = array([j for k, j in enumerate(er) if not k == i])
#            fit = fit_curvature(jnf, jns, jne)
#            jn.append((10**fit[2], log10(e)**-1*cat_flux_ref1*fit[5], fit[6]))
#            print jn[-1]
#
#        cat_predict=power_law_curvature(cat_flux_ref, array(MWA_FREQS)/REF_FREQ, cat_alpha, cat_phi)
#        cat_predict1=power_law(cat_flux_ref1, array(MWA_FREQS)/REF_FREQ, cat_alpha1)
#
#        if abs((cat_predict[0]/cat_predict1[0]) - 1) > 0.1:
#            curved="true"
#        else:
#            curved="false"
#
#        if CAT_FREQS[0] > 200:
#            extrapolated="true"
#        else:
#            extrapolated="false"
#
#        if size > 1.05:
#            resolved = "true"
#        else:
#            resolved = "false"
#
#        outline = "%s,%s,%e,%e,%e,%e,%e,%e,%e,%e,%e,%e,%e,%e,%e,%s,%s,%s," % (name, dec, mwa_flux_ref, mwa_alpha, cat_flux_ref1, cat_flux_ref1_err, cat_alpha1, cat_alpha1_err, cat_flux_ref, cat_flux_ref_err, cat_alpha, cat_alpha_err, cat_phi, cat_phi_err, cat_me1, curved, extrapolated, resolved)
#
#        outline +=','.join(["%e,%e,%e" % j for j in zip([b[0] for b in jn], [b[1] for b in jn], [b[2] for b in jn])])
#        print >> outfile, outline
#        outfile.flush()
#
        if DOPLOT:
            xmin = 50
            xmax = 5000
            name = "%07d" % i
            pltfreq = np.logspace(np.log10(xmin), np.log10(xmax), 50)
            plt.errorbar(freqs, fluxes,  yerr=flux_errors, fmt='o', color='#AAAAFF', label='Catalog flux')
            plt.plot(pltfreq, power_law(flux_ref1,  pltfreq/REF_FREQ, alpha1),  color='#AAAAFF',  label=r'$\nu_{180}$ %4.2f$\pm$%4.2f $\alpha$=%+5.2f$\pm$%4.2f' % (flux_ref1, flux_ref1_err, alpha1, alpha1_err))
            if curvature:
                plt.plot(pltfreq, power_law_curvature(flux_ref,  pltfreq/REF_FREQ, alpha, phi), ls='--', color='#AAAAFF',   label=r'$\nu_{180}$ %4.2f$\pm$%4.2f $\alpha$=%+5.2f$\pm$%5.2f $\phi$=%+5.2f$\pm$%5.2f' % (flux_ref, flux_ref_err, alpha, alpha_err, phi, phi_err))
            #plt.legend(fontsize='xx-small') #doesn't work
            plt.legend()
            plt.title("%s" % name)
            plt.xscale('log')
            plt.xlim(xmin, xmax)
            plt.ylim(1e-2, 1e4)
            plt.yscale('log')
            plt.xlabel("Frequency/MHz")
            plt.ylabel("S_int/Jy")
            plt.savefig(os.path.join(OUTDIR, "%s.png" % name))
            #plt.show()
            plt.close()
