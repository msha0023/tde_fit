"""
Contains the constants for unit conversions
Values obtained from:
https://www.bipm.org/documents/20126/41483022/SI-Brochure-9-EN.pdf
https://en.wikipedia.org/wiki/Stefan–Boltzmann_law
"""

# Energy & temperature
keV_to_erg  = 1.6022e-9       # erg / keV
kb          = 1.380649e-16    # Boltzmann constant in erg / K
hplanck     = 6.62607015e-27  # Planck constant in erg·s
steboltz    = 5.670374419e-5  # Stefan–Boltzmann constant in erg / (cm^2·K^4·s)
weinconst   = 5.88e10         # Wien's displacement constant in Hz·K

# Speeds & distances
c           = 2.99792458e10   # Speed of light in cm / s
cm_to_nm    = 1e7             # nm / cm
au          = 1.4959787e13    # cm / AU

# Time
sec_to_days = 3600.0 * 24.0   # s / day

# Derived conversions
keV_to_Hz   = keV_to_erg / hplanck  # Hz per keV

# Solar units
L_sun       = 3.846e33
