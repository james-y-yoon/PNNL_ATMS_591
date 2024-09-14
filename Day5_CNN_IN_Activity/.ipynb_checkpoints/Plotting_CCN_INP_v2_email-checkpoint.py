# Code written to plot vertical profiles of CCN, INP, and 
# vertical distribution of CCN and feature mask
# Code written by Gourihar Kulkarni to demonstrate how RNCCN VAP from ARM can be 
# used to understand the CCN and INP budgets.
# Learning Objective: What is the CCN and INP budget in the atmosphere?

import netCDF4
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd   
import xarray as xr

#Tasks after successfuly running this code. This code plots 4 figures.
# 1) Use CCN3 for SS = 0.2% and plot the INP
# 2) Plot heat map for different Nccn vs. SS
# 3) Use FF = 0.01 and Nccn for SS = 0.2; plot the heat map for INP.



fpath = ('C:/Users/D3X090/OneDrive - PNNL/GK/Projects/Texas_Lecture/')
fname = "sgprnccnprof1kulkarniC1.c1.20230521.000500.nc"
nc = netCDF4.Dataset(fpath+fname)

file_details = xr.open_dataset(fpath+fname)
print(file_details.info())

# Read the required variables
height = nc.variables['height'][:]    # Read 'height'
CCN2   = nc.variables['ccn_2'][:]     # Read 'ccn_2' (SS = 0.1%)
CCN4   = nc.variables['ccn_4'][:]     # Read 'ccn_4' (SS = 0.4%)
CCN6   = nc.variables['ccn_6'][:]     # Read 'ccn_6' (SS = 1%)

SS  = nc.variables['supersaturation_setpoint'][:]    
print(SS) 
cbh  = nc.variables['cbh'][:]    
print(cbh) 

feature_mask  = nc.variables['feature_mask'][:]  


shape = CCN2.shape
print(shape)  

shape2 = height.shape
print(shape2) 

start = 61 #103
end   = 67   #108

CCN2_sub = CCN2[start:end]  # 17th UTC hour start = will be 103
CCN4_sub = CCN4[start:end]  
CCN6_sub = CCN6[start:end]  

shape4 = CCN2_sub.shape
print(shape4)  

# Function to compute mean excluding zero and -ve values along a specific axis
def mean_excluding_zeros(arr, axis):
    mask = arr > 0
    sum_ = np.sum(arr * mask, axis=axis)
    count = np.sum(mask, axis=axis)
    return sum_ / count

# Calculate the mean of each column
CCN2_sub_mean = mean_excluding_zeros(CCN2_sub , axis=0)
CCN4_sub_mean = mean_excluding_zeros(CCN4_sub , axis=0)
CCN6_sub_mean = mean_excluding_zeros(CCN6_sub , axis=0)

shape3= CCN2_sub_mean.shape
print(shape3) 

# CCN plotting
plt.figure(1)

# Create the plot
plt.plot(CCN2_sub_mean, height, 'k', label='CCN2')
plt.plot(CCN4_sub_mean, height, 'r', label='CCN4')
plt.plot(CCN6_sub_mean, height, 'c', label='CCN6')

plt.xscale('log')
plt.ylim([0, 4])
plt.xlim([10, 10000])

plt.tick_params(axis='both', which='both', length=5, width=1)
plt.minorticks_on()

plt.xlabel('Cloud nucleating particles budget (#/cc)')
plt.ylabel('Height (km)')

plt.legend()

plt.grid(True, which='both', linestyle='--', linewidth=0.5)
#plt.show()

#plt.close(1)
#%%

# Parameters for INP calculations
Temp1 = -34.4
FF1 = 2.5e-02
INP_Temp1_CCN4 = CCN4_sub_mean * FF1

Temp2 = -20.9
FF2 = 3.55e-05
INP_Temp2_CCN4 = CCN4_sub_mean * FF2

# CCN and INP plotting
plt.figure(2)

plt.plot(CCN2_sub_mean, height, 'k', label='CCN2(0.1%)')
plt.plot(CCN4_sub_mean, height, 'r', label='CCN4(0.4%)')
plt.plot(CCN6_sub_mean, height, 'c', label='CCN6(1.0%)')

plt.plot(INP_Temp1_CCN4, height, marker='o', linestyle='--', color='red', label='INP1(-34.4)')
plt.plot(INP_Temp2_CCN4, height, marker='s', linestyle='--', color='red', label='INP2(-20.9)')


plt.xscale('log')
plt.ylim([0, 4])
plt.xlim([0.001, 10000])

plt.tick_params(axis='both', which='both', length=5, width=1)
plt.minorticks_on()

plt.xlabel('Cloud nucleating particles budget (#/cc)')
plt.ylabel('Height (km)')


plt.legend()

plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.show()







#%%
# Heat map plotting of N_CCN or scaled image of Nccn data

import matplotlib.colors as mcolors



ccn_ghan_SS = CCN2.T # Transpose the data
ccn_ghan_SS[ccn_ghan_SS == -9999] = np.nan
ccn_ghan_SS[np.isnan(ccn_ghan_SS)] = 0

# Parameters
x1 = [1, 12, 24, 36, 48, 60, 72, 84, 96, 108, 120, 132, 144]
x = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]
y1 = [17, 34, 51, 68]
y = [1000, 2000, 3000, 4000]


fig, ax = plt.subplots()

# Define color limits and colormap
clim = [1, 3000]



norm = mcolors.LogNorm(vmin=clim[0], vmax=clim[1])
cax = ax.imshow(ccn_ghan_SS, norm=norm, cmap='viridis', aspect='auto')

# Add a colorbar
cbar = fig.colorbar(cax, ax=ax)
cbar.set_ticks([1, 10, 100, 1000])
cbar.set_ticklabels(['1', '10', '100', '1000'])




cbar.set_label('N_ccn /cc')

# Set axis labels and ticks
ax.set_yticks(y1)
ax.set_yticklabels(y)
ax.set_xticks(x1)
ax.set_xticklabels(x)
ax.set_xlabel('Time in UTC (HH)')
ax.set_ylabel('Height (m)')

ax.set_ylim(68)

# Set y-axis direction
ax.invert_yaxis()
plt.show()

#%%





# Heat map plotting of feature mask or scaled image of feature mask
feature_maskT = feature_mask.T

fig, ax = plt.subplots()

# Define color limits and colormap
clim = [1, 101]
norm = mcolors.BoundaryNorm(boundaries=[1, 3, 5, 9, 21, 37, 101], ncolors=7)
cmap = mcolors.ListedColormap([
    [1, 0, 0],   # red
    [0, 1, 0],   # green
    [1, 0, 1],   # magenta
    [0.75, 0.75, 0.75],   # silver
    [0, 1, 1],   # cyan
    [0, 0, 1],   # blue
    [0.5, 0.5, 0.5]  # gray
])
cax = ax.imshow(feature_maskT , norm=norm, cmap=cmap, aspect='auto')

# Add a colorbar
cbar = fig.colorbar(cax, ax=ax, ticks=[1, 3, 5, 9, 21, 37, 101])
cbar.set_ticklabels(['no feature', 'aerosol', 'clouds', 'rain', 'liq cloud', 'ice cloud', 'hor ori ice cloud'])
cbar.set_label('Feature mask')

# Set axis labels and ticks
ax.set_yticks(y1)
ax.set_yticklabels(y)
ax.set_xticks(x1)
ax.set_xticklabels(x)
ax.set_xlabel('Time in UTC (HH)')
ax.set_ylabel('Height (m)')
ax.set_ylim(68)
# Set y-axis direction
ax.invert_yaxis()

plt.show()
#%%