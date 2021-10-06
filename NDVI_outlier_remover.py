# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 19:10:01 2021

@author: Utilizador (Joao Martins)

Program for removing outliers from NDVI data time-series data (this an example just for 1 pixel)

"""
#%%
import matplotlib.pyplot as plt
import copy
import statistics as s

# 1. Reading data from the text file and extracting only NDVI data
# First column of txt corresponds to pixel ID, followed by row and column which are 
# the index for the row and column in the entire satellite image

with open('NDVI_data_2000_2014.txt', 'r') as f:
    ndvi_data = f.read().split(",")[3:]

# 2. Converting NDVI to float
ndvi_float = list(map(float, ndvi_data))

# 3. Looping over all time-periods in the time-series and replacing all outliers 
# with the median calculated from a 7-cell window which includes the cell to be replaced
# The value is an outlier if the NDVI value in the middle of the moving window is <75% of the median or >125%

upper_threshold = 1.25
lower_threshold = 0.75

# If the middle value is not an outlier it is moved to a new list without outliers
# If the value is an outlier it is replaced with the median of the moving window

# New list corresponding to NDVI data without outliers
ndvi_out = copy.deepcopy(ndvi_float)

for i, v in enumerate(ndvi_float):
    if i < 3:
        smaller_left_window = ndvi_float[:i+4]
        median_val = s.median(smaller_left_window)
    elif i >= 3 and i < len(ndvi_float) - 3:
        size7_window = ndvi_float[i-3:i+4]
        median_val = s.median(size7_window)
    elif i >= len(ndvi_float) - 3:
        smaller_right_window = ndvi_float[(i - 3) - len(ndvi_float):]
        median_val = s.median(smaller_right_window)

    if v < median_val * lower_threshold or v > median_val * upper_threshold:
        ndvi_out[i] = median_val
    
# 4. Saving the time-series without outliers as a text file. 
no_outliers_file = 'NDVI_data_2000_2014_no_outliers.txt'

# Creating blank file (blanks the file each time code is run)
with open(no_outliers_file, 'w') as f:
    pass

# Putting ndvi_out list's floats in string format
ndvi_out_str = [str(i) for i in ndvi_out]
ndvi_out_to_txt = copy.deepcopy(ndvi_out_str)

# Adding extra commas for writing on .txt file
for i, v in enumerate(ndvi_out_str):
    if i < len(ndvi_out) - 1:
        ndvi_out_to_txt.insert((2 * i) + 1, ", ")

# Writing to file
with open(no_outliers_file, 'a') as f:
    f.writelines(ndvi_out_to_txt)

# 5. Check out results by plotting original NDVI and NDVI with outliers detected and removed.
y_original = ndvi_float
y_outl_removed = ndvi_out
x = [i for i in range(len(ndvi_float))]


plt.plot(x, y_original, label='Original NDVI')
plt.plot(x, y_outl_removed, label='Outliers Removed')
plt.title('Original NDVI and NDVI with outliers removed')
plt.xlabel('Time (8-day periods)')
plt.ylabel('NDVI (Scaled)')
plt.legend(loc = 'best')
plt.show()

# %%
