"""
Contains class for creating a light curve object
The class is used to load the light curve data from a file, fit the data to a blackbody spectrum, and plot the results.
"""
import os
import numpy as np
import scipy.integrate as integrate
import scipy.optimize as optimize
import re
from .lightcurve_plot import Lightcurveplot
from ..utils.constants import c, cm_to_nm, sec_to_days, steboltz, kb, keV_to_erg
from ..utils.conversions import nm_to_keV
from .physics import Bnu, Wien_T_from_nu, Bnulog, get_lum_by_rad, get_Lbol
from ..utils.survey_bands import ztfmin_Hz, ztfmax_Hz, swiftmin_Hz, swiftmax_Hz

class LightCurve(Lightcurveplot):
    """
    A class to represent a light curve.

    Attributes
    ----------
    filename : str
        The name of the file containing the light curve data. Obtained from SPLASH.

    Methods
    -------
    __init__(filename)
        Initializes the LightCurve object with the given filename.
    load_data()
        Loads the light curve data from the file.
    plot()
        Plots the light curve.
    """

    def __init__(self, filepath):
        """
        Constructs all the necessary attributes for the LightCurve object
        """

        self.folder, self.name = os.path.split(filepath)

        self.filename = filepath

        # Test file existence
        try:
            self.data = self.load_data()
        except FileNotFoundError:
            raise FileNotFoundError(f"File {self.filename} not found.")
        except Exception as e:
            raise RuntimeError(f"An error occurred while loading the data: {e}")

        
        # Test data shape
        if self.data.ndim != 2 or self.data.shape[1] != 2:
            raise ValueError(f"Data in {self.filename} must be a 2D array with two columns.")
        
        # Test file is not empty
        if self.data.size == 0:
            raise ValueError(f"Data in {self.filename} is empty.")
        
        self.nu_grid                   = self.data[:,0]
        self.spec                      = self.data[:,1]
        self.spec[self.spec == np.inf] = 0
        self.lam                       = (c/self.nu_grid)
        self.Tguess                    = 1e4
        self.Tguessx                   = 1e5

    def load_data(self):
        data = np.array(np.loadtxt(self.filename))
        return data
    

    def get_color_temperature(self):
        """
        Colour temperature, by fitting to peak of spectrum
        """
        imax = np.argmax(self.spec)
        
        Tc = Wien_T_from_nu(self.nu_grid[imax])

        if (Tc > 1.):
            bb_scale = self.spec[imax]/Bnu(self.nu_grid[imax],Tc,1.0)
        else:
            bb_scale = 0.

        return Tc, bb_scale

    def fit_Tc(self):

        Tc, bb_scale = self.get_color_temperature()
        bbspec = Bnu(self.nu_grid, Tc, bb_scale)
        
        return Tc, bb_scale, bbspec

    def get_convolved_spectrum(self, nu_min, nu_max):
        myspec = []
        mylam  = []
        mynu   = []

        for i, val in enumerate(self.spec):
            if (self.nu_grid[i] >= nu_min and self.nu_grid[i] <= nu_max and self.spec[i] > 1e9):
                myspec.append(self.spec[i])
                mynu.append(self.nu_grid[i])
                mylam.append(c / self.nu_grid[i] * cm_to_nm)

        return mylam, mynu, myspec

    def fit_band(self, minHz, maxHz, x=False):
        # get convolved spectrum
        mylam, mynu, myspec = self.get_convolved_spectrum(minHz, maxHz)
        Tc, bb_scale        = self.get_color_temperature()

        # return zeros if no emission in band
        if (np.all(myspec < 1.e-30) or np.size(myspec) <= 2):
            return 0., 0., Bnu(self.nu_grid, 0., 0.)

        # fit single temperature blackbody to data
        fit_spec = np.log(myspec)

        if x:
            popt, pcov = optimize.curve_fit(Bnulog, mynu, fit_spec, p0=(self.Tguessx, bb_scale))
        else:
            popt, pcov = optimize.curve_fit(Bnulog, mynu, fit_spec, p0=(self.Tguess, bb_scale))
           
        Tfit, bb_scale = popt
        print(np.sqrt(np.diag(pcov)))
       
        bbspec = Bnu(self.nu_grid, Tfit, bb_scale)
        return Tfit, bb_scale, bbspec

    
    def get_time_from_filename(self):
        
        m = re.search(r'_(\d\d\d\d\d)(.*).spec',self.filename)
        if m:
            itime = m.group(1)
            file='lightcurve_'+self.name[:-5]+'.out'

            if not os.path.exists(file):
                raise FileNotFoundError(f"Associated lightcurve file {file} not found.")
    
            try:
                row = np.loadtxt(file)
            except:
                print("failed to load "+file)

            # get information from lightcurve file
            time = row[0] / sec_to_days
            Ltot = row[1]
            Reff = row[2]
            Teff = row[3]
        else:
            print("failed to match time from "+file)
            time = 0.
            
        return time, Ltot, Reff, Teff
    
    def write_data(self):
        files = ['lum.dat', 'tde-lightcurve.out']
        self._delete_existing_files(files)
        
        time, Ltot, Reff, Teff = self.get_time_from_filename()
        Tc, Tbb, Tx, l_bb, l_bb2, l_x, rbb, rbb2, rbbtot, rx, lbb_to_lx = self._compute_fits(Ltot)

        self._write_lum_dat(files[0], time, l_bb, rbb, Tbb, Ltot, l_x, rx, Tx)
        self._write_tde_lightcurve(files[1], time, Ltot, Teff, Reff, l_bb, Tc, rbb,
                                l_bb2, Tbb, rbb2, rbbtot, l_x, Tx, lbb_to_lx)


    def _delete_existing_files(self, filenames):
        for file in filenames:
            if os.path.isfile(file):
                print(f"File {file} already exists. Deleting.")
                os.remove(file)
            print(f"Creating file {file}.")


    def _compute_fits(self, Ltot):
        Tc, bbscale, _ = self.fit_Tc()
        l_bb = get_Lbol(Tc, bbscale)

        Tbb, bbscale, _ = self.fit_band(ztfmin_Hz, ztfmax_Hz)
        l_bb2 = get_Lbol(Tbb, bbscale)
        self.Tguess = Tbb

        Tx, bbscale, _ = self.fit_band(swiftmin_Hz, swiftmax_Hz, x=True)
        l_x = get_Lbol(Tx, bbscale)
        self.Tguessx = Tx

        lbb_to_lx = l_bb / l_x if l_x > 0 else 0.

        rbb = np.sqrt(l_bb / get_lum_by_rad(Tc)) if Tbb > 0 else 0.
        rbb2 = np.sqrt(l_bb2 / get_lum_by_rad(Tbb)) if Tbb > 0 else 0.
        rbbtot = np.sqrt(Ltot / get_lum_by_rad(Tbb)) if Tbb > 0 else 0.
        rx = np.sqrt(l_x / get_lum_by_rad(Tx)) if Tx > 0 else 0.

        if Tbb > 0:
            print(f"Tc = {Tc}, Lbol = {l_bb}")
            print(f"Tbb = {Tbb}, Lbol = {l_bb2}")
            print(f"Tx = {Tx * kb / keV_to_erg:.2f} keV, Lx = {l_x}, Lbb/Lx = {lbb_to_lx}")

        return Tc, Tbb, Tx, l_bb, l_bb2, l_x, rbb, rbb2, rbbtot, rx, lbb_to_lx


    def _write_lum_dat(self, filename, time, l_bb, rbb, Tbb, Ltot, l_x, rx, Tx):
        with open(filename, 'w') as f:
            f.write('# time   lbb   rbb   Tbb   ltot   lx   rx   Tx\n')
            f.write(f'{time:.5e} {l_bb:.5e} {rbb:.5e} {Tbb:.5e} {Ltot:.5e} {l_x:.5e} {rx:.5e} {Tx:.5e}\n')


    def _write_tde_lightcurve(self, filename, time, Ltot, Teff, Reff, l_bb, Tc, rbb,
                             l_bb2, Tbb, rbb2, rbbtot, l_x, Tx, lbb_to_lx):
        with open(filename, 'w') as f:
            f.write('# Time [days],Ltot [erg/s],T_{eff} [K],R_{eff} [cm],l_bb [erg/s],Tc [K],R_{bbfit} [cm],'
                    'l_{bol} [erg/s],T_{bb} [K],R_{bb} [cm],R_{bbtot} [cm],L_x [erg/s],Tx [keV],L_{bb}/L_x\n')
            f.write(f'{time:.5fe} {Ltot:.5e} {Teff:.5e} {Reff:.5e} {l_bb:.5e} {Tc:.5e} {rbb:.5e} '
                    f'{l_bb2:.5e} {Tbb:.5e} {rbb2:.5e} {rbbtot:.5e} {l_x:.5e} {Tx * kb / keV_to_erg:.5e} {lbb_to_lx:.5e}\n')
