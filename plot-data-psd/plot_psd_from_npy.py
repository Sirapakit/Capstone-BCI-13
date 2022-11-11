import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import plotly.express as xp
# import plotly.io as pio; pio.renderers.default = "iframe"
from scipy import signal

path = r'../dataset/chb15/npy/data_chb15_06.npy'
filename = r'data15_06.csv'
df = pd.read_csv(filename) #load the data
df = df.set_index(df.columns[0]) #set the first column as the index

fig, ax = plt.subplots() #create an empty plot

df.plot(ax=ax) #use the dataframe to add plot data, tell it to add to the already created axes

ax.set(xlabel='Time (s)',
       ylabel='Acceleration (g)',
       title=filename)
ax.grid() #turn on gridlines

fig.savefig('full-time-history.png')
plt.show()