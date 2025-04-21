"""
Contains class to analyse multiple files, save results, and plot results all in one go.
"""

import os
import matplotlib.pyplot as plt
from .lightcurve import LightCurve

class PipeLine:
    """
    Class to analyse multiple files, save results, and plot results all in one go.
    It also provides methods to plot the light curve and spectrum of each file.
    """
    def __init__(self, foldername):
        self.foldername = foldername
        self.time = []
        self.Ltot = []
        self.Reff = []
        self.Teff = []
        self.Tc = []
        self.Tbb = []
        self.Tx = []
        self.l_bb = []
        self.l_bb2 = []
        self.l_x = []
        self.rbb = []
        self.rbb2 = []
        self.rbbtot = []
        self.rx = []
        self.lbb_to_lx = []
    
    def read_all_files(self):

        # create a folder for saving the plots
        self.plot_folder = os.path.join(self.foldername, "plots")
        os.makedirs(self.plot_folder, exist_ok=True)

        for filename in os.listdir(self.foldername):
            print(filename, "filename")
            if filename.endswith(".spec"):
                filepath = os.path.join(self.foldername, filename)
                print(f"Processing file: {filepath}")
                
                try:
                    lc = LightCurve(filepath)
                    data = lc.write_all_data()
                    self._fill_arrays(*data)

                    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
                    lc.plot_spec(ax1)
                    lc.plot_lightcurve(ax2, self.time, self.Ltot, self.l_bb)

                     # Save the plots
                    fig.savefig(os.path.join(self.plot_folder, "lightcurve_"+str(filename)+".png"))
                    print(f"Saved plot for {filename} to {self.plot_folder}")
                    

                except Exception as e:
                    print(f"Error processing file {filename}: {e}")
        
        # Save the collected data
        LightCurve.write_multiple_data(self.foldername,
            self.time, self.Ltot, self.Reff, self.Teff, self.Tc,
            self.Tbb, self.Tx, self.l_bb, self.l_bb2, self.l_x,
            self.rbb, self.rbb2, self.rbbtot, self.rx, self.lbb_to_lx
        )
        
        
    # Fill the arrays with data
    def _fill_arrays(self, time, Ltot, Reff, Teff, Tc, Tbb, Tx, l_bb, l_bb2, l_x, rbb, rbb2, rbbtot, rx, lbb_to_lx):
        self.time.append(time)
        self.Ltot.append(Ltot)
        self.Reff.append(Reff)
        self.Teff.append(Teff)
        self.Tc.append(Tc)
        self.Tbb.append(Tbb)
        self.Tx.append(Tx)
        self.l_bb.append(l_bb)
        self.l_bb2.append(l_bb2)
        self.l_x.append(l_x)
        self.rbb.append(rbb)
        self.rbb2.append(rbb2)
        self.rbbtot.append(rbbtot)
        self.rx.append(rx)
        self.lbb_to_lx.append(lbb_to_lx)

    def plot_lum_data_all(self):
        LightCurve.plot_lum_data(
            self.l_bb, self.Ltot, self.Tbb, self.Reff, self.time, self.plot_folder,
        )
    
    

    
        
    


