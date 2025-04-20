"""
Contains the wavelength and frequency ranges for the ZTF and Swift surveys
"""

from .conversions import keV_to_nm
from .constants import c, keV_to_Hz, cm_to_nm

# SWIFT survey
swiftmin_keV = 0.3
swiftmax_keV = 10.0
swiftmin_Hz  = swiftmin_keV*keV_to_Hz
swiftmax_Hz  = swiftmax_keV*keV_to_Hz
swiftmin_nm  = keV_to_nm(swiftmax_keV)
swiftmax_nm  = keV_to_nm(swiftmin_keV)

# ZTF survey
ztfmin_nm    = 367.6 #180 #408.6 #180. #408.6
ztfmax_nm    = 901.0 #888.37
ztfmin_Hz    = c/(ztfmax_nm/cm_to_nm)
ztfmax_Hz    = c/(ztfmin_nm/cm_to_nm)
ztfmin_keV   = ztfmin_Hz/keV_to_Hz
ztfmax_keV   = ztfmax_Hz/keV_to_Hz