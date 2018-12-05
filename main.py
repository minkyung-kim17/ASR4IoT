## Dynamic sample rate adaptation for long-term IoT sensing applications
## https://ieeexplore.ieee.org/document/7845437

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style='darkgrid',color_codes=True)

from collections import deque
import bb_model 

## Load data 
data=np.load('Data/temp.npy') # 2d format (Days*Time(288, 5min.))
data=np.reshape(data, (1,-1)).squeeze() # Assume real time data

## Model adjusting sample rate adaptively with real time series data
# User-defined parameter
prevN=32
k=1
tmax=5
phi=1

# model
bb_model=bb_model.bb_model(prevN=prevN,k=k,tmax=tmax,phi=phi)

## Simulation
# ~prevN
Ds=deque(data[0:prevN]) # data that must be stored in real time / or you can store whole data

# prevN~
twait=tmax
sampt=prevN # adjusting sample rate starts at prevN
sampIdxes=np.zeros(np.size(data)) # data를 얼마나 입력받을지 모르니까, 미리 만들어 놓는게 사실 말은 안되지만..., mark 1 when sampled 
sampData=np.zeros(np.size(data))*np.nan # 여기도 마찬가지  
for t in range(prevN, len(data)):
	# Ds=data[t-prevN+1:t+1] # for calculate_twait, sliced data with prevN
	Ds.append(data[t])
	Ds.popleft()

	if t==sampt:
		sampIdxes[t]=1 # mark
		sampData[t]=data[t] 
		dyn=bb_model.calculate_dyn(t, Ds, option='vd')
		twait=bb_model.calculate_twait(tmax,dyn)
		sampt=t+twait

		print('Current time: ', t, '\t|| Sample rate: ', twait, '\t|| Next sample time: ', sampt)

## Visualize 
bb_model.visualize(data,sampData,sampIdxes,visualizeLength=288) 

