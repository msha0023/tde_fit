tde_fit 🌠

A Python package to analyze spectral and photometric data from PHANTOM TDE simulations
tde_fit is a Python package designed to streamline the analysis of spectral and photometric data from PHANTOM TDE simulations. It allows you to:
Load simulation output files
Fit blackbody models to spectra
Calculate key physical quantities (e.g., bolometric and X-ray luminosities)
Automatically save plots and derived data
Compare synthetic and observed lightcurves

🛠️ Installation

git clone https://github.com/msha0023/tde_fit.git
cd tde_fit
pip install .
Requirements (Python 3.8+):
numpy
scipy
matplotlib

📁 Project Structure

tde_phantom/
├── src/
│   └── tde_fit/
│       ├── core/
│       │   ├── lightcurve.py
│       │   ├── lightcurve_plot.py
│       │   ├── pipeline.py
│       │   ├── plot_lum.py
│       │   └── physics.py
│       ├── utils/
│       │   ├── constants.py
│       │   └── conversions.py
│       └── Data_Observations/

🚀 Quickstart

1. Batch-process and plot simulation spectra
from tde_fit import PipeLine

m = PipeLine('data')               # Folder with .spec and lightcurve files
m.read_all_files()                # Processes all files, saves plots to 'data/plots',
                                  # and generates 'tde-lightcurve.out'
2. Plot archival or observational lightcurve data
from tde_fit import PlotLum

m = PlotLum('/path/to/lightcurve_folder')  
# Provide a parent folder with subfolders, each containing a tde-lightcurve.out
m.plot_figure()

3. Plot individual .spec files
from tde_fit.core.lightcurve import LightCurve

m = LightCurve('folder_name/filename.spec')
m.plot_spectrum()    # Plots the spectrum for the given file