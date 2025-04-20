"""
Contains functions to calculate the physical properties of the TDE.
The functions are used to calculate the mass, radius, and luminosity of the TDE.
"""

from ..utils.constants import c, hplanck, kb, weinconst, steboltz
import numpy as np

def Bnu(nu, temp, bbscale):
    """
       Planck function
    """
    if (temp <= 1.):
       return 0.        
    hnu_on_kT  = hplanck * nu / (kb * temp)
    hnu3_on_c2 = hplanck * nu**3 / c**2

    Bnu = 2. * hnu3_on_c2 / (np.exp(hnu_on_kT) - 1.)
    return Bnu * bbscale

def Bnulog(nu, temp, bbscale):
    return np.log(Bnu(nu, temp, bbscale))

def Wien_T_from_nu(nu):
    """
       Wien's displacement law, T from nu
    """
    return nu / weinconst

def get_Lbol(Tc,bb_scale):
    """
       integrate blackbody fit to get bolometric luminosity
    """
    lum = 4. * steboltz * Tc**4 * bb_scale
    return lum

def get_lum_by_rad(temp):
      val = (4. * np.pi * steboltz * temp**4)
      return val


