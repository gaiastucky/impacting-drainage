# -*- coding: utf-8 -*-
"""
Does drainage change with impacting?
-Do large canyons get preferential preservation?
-How much does this change?
-On Mars, 24% of eroded volume is from outflow lakes, is this
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import r2_score
import scipy
from impacting_functions import clean_profiles, split_rivers



#%% Load data
fogo = 'profile_data/fogo_profiles.csv' #Fogo island river data points file
kohala = 'profile_data/kohala_profiles.csv' #Fogo island river data points file
df_f = clean_profiles(pd.read_csv(f'{fogo}'),'e_p_a_au') #resolution and extra data (res = 5 m)
df_k = clean_profiles(pd.read_csv(f'{kohala}'),'e_p_a_au') #resolution and extra data (res = 5 m)

#%% Edit data
#Fogo = continuous
#Hawaii = bimodal
canyons=[107, 120, 164, 168, 150, 160, 155] #Deep basins (canyons in kohala)
df = split_rivers(df_k, canyons)

#%% Plotting data: Erosion distribution
sns.set_theme(style="white")
bins=30
sns.histplot(data=df_f, x="Erosion_m", log_scale=True, kde=True, bins=bins, cumulative=False) #element="poly",plt.show()
plt.show()
sns.histplot(data=df_k, x="Erosion_m", hue="Type", log_scale=True, kde=True, bins=bins, cumulative=False) #element="poly",
plt.show()

#%% Plot rivers (areals)
sns.relplot(x='X_m', y='Y_m', hue='Erosion_m', size='Erosion_m', sizes=(0.1,5), data=df_f)
plt.show()
sns.relplot(x='X_m', y='Y_m', hue='Erosion_m', size='Erosion_m', sizes=(0.1,5), data=df_k)
plt.show()