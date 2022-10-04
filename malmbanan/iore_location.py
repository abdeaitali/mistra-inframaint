# -----------------------------------------------------------------
#                                                   Initiate
#                                                   ---------------

# Import packages
import os
import pandas as pd
import geopandas as gpd
import matplotlib as mp
import matplotlib.pyplot as plt
from functions import convert
import numpy as np

# Paths
home = os.getcwd()
r_path = os.path.abspath(os.path.join(home,'DATA/sve_1milj_Sweref_99_TM_shape/svk/riks'))
r_path_iore = os.path.abspath(os.path.join(home,'DATA'))

# -----------------------------------------------------------------
#                                                   Load iore-data
#                                                   ---------------

# File name
filename = 'IORE127_Export_From_20201221_To_20201223.csv'
file_iore = os.path.join(r_path_iore,filename)
wb = pd.read_csv(file_iore)
colab_1 = 'DetectionPoint (lat)'; colab_2 = 'DetectionPoint (lon)'
w=pd.DataFrame(wb,columns=[colab_1,colab_2])
n = np.size(w,0)
coord_iore = np.zeros((n-1,2))
for i in range(1,n):
    lat = w[colab_1][i]
    lon = w[colab_2][i]
    E,N = convert(lon,lat)
    coord_iore[i-1,:] = [E,N]


# -----------------------------------------------------------------
#                                                   Load maps
#                                                   ---------------

# Files
file_1 = 'my_riks.shp'
file_2 = 'JL_riks.shp'
file_3 = 'MB_riks.shp'

# File name
map_1 = os.path.join(r_path,file_1)
map_J = os.path.join(r_path,file_2)
map_B = os.path.join(r_path,file_3)

# Select region
xmin = 577646;ymin=7512310;xmax=756476;ymax=7619270
bbox = (xmin,ymin,xmax,ymax)
#bbox=(600000,7100000,750000,7200000)


# -----------------------------------------------------------------
#                                                   Figures
#                                                   ---------------

# Plot figure
map_df = gpd.read_file(map_1,bbox=bbox)
map_df_J = gpd.read_file(map_J,bbox=bbox)
map_df_B = gpd.read_file(map_B,bbox=bbox)
#map_df = gpd.read_file(map_1)
#map_df.head()
ax=map_df[(map_df["KKOD"] == 3) | (map_df["KKOD"] == 1)].plot(figsize=(8, 4))
map_df_J[(map_df_J["KKOD"] == 5611) | (map_df_J["KKOD"] == 5612) | (map_df_J["KKOD"] == 5621) | (map_df_J["KKOD"] == 5651)].plot(ax=ax,edgecolor='black')
map_df_B.plot(ax=ax,edgecolor='black',facecolor='black')
ax.plot(coord_iore[:,1],coord_iore[:,0],'ro',markersize=1)
#(map_df_B["KKOD"] == 432) | (map_df_B["KKOD"] == 433) | (map_df_B["KKOD"] == 435) | (map_df_B["KKOD"] == 434)
ax.tick_params(axis="both", labelsize=12)
plt.xlabel(r'$\itx$' ' [m]',fontsize=14)
plt.ylabel(r'$\ity$' ' [m]',fontsize=14)
plt.xlim(550000,750000)
plt.ylim(7500000,7620000)
plt.tight_layout()
#plt.show()
plt.savefig('map_iore.jpg',bbox_inches='tight')


# 


