"""
Contains the Lightcurveplot class, which is used to plot the light curve and spectrum of a TDE.
The class provides methods to plot the fitted spectrum and the filter bands based on the ZTF and SWIFT surveys.
"""

from ..utils.constants import keV_to_Hz
from ..utils.survey_bands import swiftmin_keV, swiftmax_keV, ztfmin_keV, ztfmax_keV
from ..utils.conversions import nm_to_keV
import matplotlib.pyplot as plt
import numpy as np

class Lightcurveplot:
    """
    Class to plot the light curve and spectrum of a TDE.
    The class provides methods to plot the fitted spectrum and the filter bands based on the ZTF and SWIFT surveys.
    """
    def plot_spectrum(self):
        """
        Plot the fitted spectrum on the given axis.
        """
        energ = self.nu_grid / keV_to_Hz
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(energ, self.spec*self.nu_grid, ls='dotted')
        ax.set_xlabel(r'Energy (keV)', fontsize=16)
        ax.set_ylabel(r'Flux (erg/s/cm$^2$)', fontsize=16)
        ax.set_xscale('log')
        ax.set_yscale('log')
        plt.show()

        return
    
    def plot_spec(self,ax1=None):
        """
        plot the spectrum and the filter bands based on the ZTF and SWIFT surveys
        """
        ymin = 2e35
        ymax = 1e45

        energ = self.nu_grid / keV_to_Hz
        if (ax1 is None):
            fig, ax1 = plt.subplots(figsize=(10, 6))
        else:
            fig = ax1.figure

        ax1.plot(energ,self.spec*self.nu_grid)
        self.plot_filter(ax1,energ,ymin,ymax,swiftmin_keV,swiftmax_keV,'X-ray',1.,True)
        self.plot_filter(ax1,energ,ymin,ymax,ztfmin_keV,ztfmax_keV,'Optical/UV',nm_to_keV(550),True)
        ax1.set_xscale('log')
        ax1.set_yscale('log')
        ax1.set_ylim(ymin,ymax)
        ax1.set_xlabel(r'Energy (keV)', fontsize=16)
        ax1.set_ylabel(r'Flux (erg/s/cm$^2$)', fontsize=16)

        if (ax1 is None):
            plt.show()
       
        return

    def plot_filter(self, ax, energ, ymin, ymax, lmin, lmax, label, lpos, plot_label):
        """
        Plot filter function as a vertical band
        """
        ax.fill_between(energ, ymin, ymax, where=np.logical_and(energ > lmin, energ < lmax), color='magenta', alpha=0.25)
        if (plot_label):
            ax.text(lpos, 5e35, label, ha="center", va="bottom", rotation='vertical', alpha=0.25)

        return

    def plot_lightcurve(self, ax2, times, ltots, lbbs):

        ax2.set_yscale('log')
        # ax2.set_ylim(8e42,4e44)
        ax2.set_ylim(1e41,4e44)
        ax2.set_xlim(0.,365.)
        ax2.plot(times,ltots,color='tab:blue')
        ax2.plot(times,lbbs,color='tab:orange')
        ax2.set_xlabel('Time [days]', fontsize=16)
        ax2.set_ylabel(r'L$_{bol}$ [erg/s]', fontsize=16)
    
    @staticmethod
    def plot_lum_data(lbbs, ltots, tbbs, rbbs, times, foldername):
        fig, [ax1, ax2, ax3] = plt.subplots(3,1,figsize=(6,10),sharex=True)

        ax1.plot(times,np.log10(lbbs),c='k',label=r'$L_{bb}$')
        plt.plot(times,np.log10(ltots),c='r',label=r'$L_{\rm{tot}}$')
        ax1.set_ylabel(r'log $L_{bol}$ [erg/s]')
        plt.legend()

        ax2.plot(times,np.log10(rbbs),c='k')
        ax2.set_ylabel('log R [cm]')

        ax3.plot(times,np.log10(tbbs),c='k')
        ax3.set_ylabel('log T [K]')

        ax3.set_xlabel('Time [days since first peak]')
        plt.subplots_adjust(wspace=0, hspace=0)

        filename = foldername + '/luminosity.pdf'
        plt.savefig(filename)


        
    
