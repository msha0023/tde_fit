"""
Contains the PlotLum class for loading and processing TDE simulation lightcurves.
Uses data files from the Data_Observations folder for comparison.
"""

import numpy as np
import os
import matplotlib.pyplot as plt
from ..utils.constants import cm_to_au, L_sun


class PlotLum:
    """
    Class to handle simulation lightcurve data and preprocess it
    for plotting or further analysis.
    """

    def __init__(self, foldername):
        self.foldername = foldername

        base_dir = os.path.dirname(os.path.dirname(__file__))  # this gets you to the tde_fit folder
        self.datapath = os.path.join(base_dir, 'Data_Observational/')


        # Column indices dictionary
        self.columns = {
            "lum": 3,
            "rbb": 4,
            "temp": 2,
            "lum_obs": 2,
            "rbb_obs": 4,
            "temp_obs": 6,
            "xray": 11,
        }

        # Time shift values
        self.t_shift = 0.0
        self.t_shift_sim = 40.0  

        # Data placeholders
        self.array = None            # Original loaded array
        self.array_shifted = None    # Shifted and scaled version

    def load_sim_lightcurve(self, filepath):
        """
        Loads a lightcurve from a simulation file and applies time shift
        and unit conversion.

        Parameters:
        -----------
        filepath : str
            Path to the simulation lightcurve data file.
        """
        self.array = np.loadtxt(filepath, skiprows=2)
        self.array_shifted = self._shift_to_t_since_max()

    def _get_t_at_max_lum(self):
        """
        Determines the time of peak luminosity in the simulation data,
        and stores it as self.t_shift.
        """
        lum = self.array[:, self.columns["lum"]]
        t = self.array[:, 0]

        max_index = np.argmax(lum)
        self.t_shift = t[max_index]

        if self.t_shift > 50.0:
            self.t_shift = 30.0

    def _shift_to_t_since_max(self):
        """
        Returns a copy of the data with:
        - time shifted so t=0 corresponds to peak luminosity
        - blackbody radius converted from cm to AU

        Returns:
        --------
        array : np.ndarray
            Modified lightcurve array.
        """
        self._get_t_at_max_lum()
        arr = self.array.copy()
        arr[:, 0] -= self.t_shift
        arr[:, self.columns["rbb"]] *= cm_to_au
        return arr
    
    def plot_figure(self):
        fig = plt.figure(figsize=(4.5,10.5))
        plt.subplots_adjust(left=0.15)
        fig.add_subplot(3,1,1)
        self.plot_lum()
        fig.add_subplot(3,1,2)
        self.plot_rbb()
        fig.add_subplot(3,1,3)
        self.plot_temp()
        savename = os.path.join(self.datapath, 'tde_lightcurves.pdf')
        plt.savefig(savename,bbox_inches='tight')
        plt.show()

    def plot_lum(self):
        plt.yscale('log')
        ymin=3e40
        ymax=1e45

        plt.ylim(ymin,ymax)
      
        plt.ylabel(r'L$_{bb}$ [erg/s]')

        self.plot_obs_data(self.columns["lum_obs"])
        self.plot_sim(self.columns["lum"])
        
       
        plt.legend(loc='lower right',fontsize=8,ncol=3)

        return
    
    def plot_temp(self):
        plt.yscale('log')
        ymin=8e3
        ymax=1e5

        plt.ylim(ymin,ymax)
        
        plt.ylabel('T$_{bb}$ [K]')

        self.plot_obs_data(self.columns["temp_obs"])
        self.plot_sim(self.columns["temp"])

        return

    def plot_rbb(self):
        plt.yscale('log')
        ymin=2e13;ymax=1e16
        plt.ylim(ymin,ymax)
       
        plt.ylabel(r'R$_{bb}$ [cm]')
        self.plot_obs_data(self.columns["rbb_obs"])
        self.plot_sim(self.columns["rbb"])

        plt.legend(loc='best',fontsize=9,ncol=3)
        return

    def plot_xray(self):
        plt.ylim(1.,1.e5)
        plt.ylabel('Lx / L_bb')
        self.plot_sim(self.columns["xray"])
        return

    def plot_obs_data(self, col):

        data_files = ['AryaStark_RT.dat', 'BranStark_RT.dat', 'Brienne_RT.dat',
                      'CerseiLannister_RT.dat', 'GendryBaratheon_RT.dat',
                      'JaimeLannister_RT.dat', 'JorahMormont_RT.dat',
                      'MargaeryTyrell_RT.dat', 'NedStark_RT.dat',
                      'PetyrBalish_RT.dat', 'SansaStark_RT.dat',
                      'Varys_RT.dat', 'PS1-10jh_RT.dat', 'ASASSN-14li_RT.dat']
        
        labels = ['AT2018lni', 'AT2019qiz', 'AT2019lwu', 'AT2018lna',
                  'AT2018hyz', 'AT2019azh', 'AT2018iih', 'AT2019cho',
                  'AT2018zr', 'AT2019meg', 'AT2018hco', 'AT2019bhf',
                  'PS1-10jh', 'ASASSN-14li']
        
        markers=['.','o','v','^','>','<','8','s','p','P','*','h','+','D','X','H']

        for i, file in enumerate(data_files):
            
            filepath = os.path.join(self.datapath, 'VanVelzen_et_al_data', file)
            self._plot_obs_pts(filepath, col, labels[i], markers[i])
        
        self._plot_obs_18jd(col)

        return

    def _plot_obs_pts(self, filename, col, label, marker):
        arr = np.loadtxt(filename, skiprows=1, delimiter=',')
        t = arr[:,1]  # time since peak
        y = 10**arr[:,col]

        if (col==self.columns["lum_obs"]):
            plt.scatter(t,y,s=10.0,alpha=0.35,label=label,marker=marker)
        else:
            plt.scatter(t,y,s=10.0,alpha=0.35,marker=marker)
    
    def _plot_obs_18jd(self, col):
        folder = os.path.join(self.datapath, 'assasn18jd')
        if (col==self.columns["rbb_obs"]):
            filename = os.path.join(folder, '18jd-Rbb2.txt')
            arr = np.loadtxt(filename,delimiter=',')
            t = arr[:,0]  # time since peak
            y = arr[:,1]
            plt.scatter(t,y,s=101.0,alpha=0.35)

        elif (col==self.columns["lum_obs"]):
            filename = os.path.join(folder, '18jd-lum.txt')
            arr = np.loadtxt(filename,delimiter=',')
            t = arr[:,0]  # time since peak
            y = np.log10(10**arr[:,1]*L_sun)
            plt.scatter(t,y,s=10.0,alpha=0.35,label='ASASSN-18jd')

        elif (col==self.columns["temp_obs"]):
            filename = os.path.join(folder, '18jd-logT.txt')
            arr = np.loadtxt(filename,delimiter=',')
            t = arr[:,0]  
            y = arr[:,1]
            plt.scatter(t,y,s=10.0,alpha=0.35)
    
    def plot_sim(self, col):
        plt.xlim(-25.,335.)
        self._plot_my_curves(col)
        return

    def _plot_my_curves(self, col):
        ls = 'solid'
        plt.gca().set_prop_cycle(None)
        
        # find all directories inside the foldername
        folders = os.listdir(self.foldername)

        for i, folder in enumerate(folders):
            folderpath = os.path.join(self.foldername, folder)
            filepath = os.path.join(folderpath, 'tde-lightcurve.out')

            self.load_sim_lightcurve(filepath)
            time = self.array_shifted[:,0]

            # Get current color cycle
            color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
            color = color_cycle[i % len(color_cycle)]  # where i is the index of your plot

            # if badfrac is present, use it to mask the data
            if (np.size(self.array_shifted, 1) > 14):
                badfrac = self.array_shifted[:,14]
                for iok, frac in enumerate(badfrac):
                    if (time[iok] > 10. and badfrac[iok] < 0.02):
                        break
            
            else:
                iok = len(time) - 1

            # time,Ltot,Teff,Reff,l_bb,Tc,rbb,l_bb2,Tbb,rbb2,rbbtot,Lx,Tx,Lbb/Lx,badfrac
            #   0    1    2    3    4   5  6    7    8    9    10   11 12  13    14
            if ( col==self.columns["rbb"]):
                y = self.array_shifted[:,9] #*cm_to_au
                print("rbb at 365 days is ",y[-1]*cm_to_au,time[-1])

            elif ( col==self.columns["temp"] ):
                y = self.array_shifted[:,8]
                plt.xlabel('Time since peak [days]')

            elif ( col==self.columns["lum"] ):
                y = self.array_shifted[:,7]

            elif ( col==self.columns["xray"] ):
                y = self.array_shifted[:,1] / self.array_shifted[:,11]
                plt.scatter(time,y,color='green')

            if (iok > 0):
                plt.plot(time[iok:], y[iok:], linestyle=ls, label=str(folder),c=color,alpha=1.)
                plt.plot(time[:iok], y[:iok], linestyle=ls, label="", c=color,alpha=0.3)
            else:
                plt.plot(time,y,linestyle=ls,label=str(folder),c=color,alpha=1.)

        return