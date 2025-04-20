"""
Contains functions to convert from keV to nm and vice versa
"""

from .constants import c, keV_to_Hz, cm_to_nm

# keV to nm conversion 
def keV_to_nm(energy_kev):
    energy_Hz = energy_kev*keV_to_Hz
    return c/energy_Hz*cm_to_nm

# nm to keV conversion
def nm_to_keV(lam_nm):
    energy_Hz = c/(lam_nm/cm_to_nm)
    return energy_Hz/keV_to_Hz

# keV to Hz conversion
def keV2Hz(x):
    return x * keV_to_Hz

# Hz to keV conversion
def Hz2keV(x):
    return x / keV_to_Hz

# nm to keV conversion
def nm2keV(x):
    return x / keV_to_Hz