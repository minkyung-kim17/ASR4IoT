
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style='darkgrid',color_codes=True)

class bb_model():
	def __init__(self, prevN, k, tmax, phi):
		## Set user-defined parameters
		self.prevN=prevN # size of moving average window
		self.k=k # width of bollinger bands
		self.b=2*k # to adjust the distance between the considered Bollinger Bands
		self.tmax=tmax
		self.phi=phi

	def calculate_dyn(self, t, Ds, option):
		Ds=np.array(Ds)
		bbmid=np.sum(Ds)/self.prevN
		sigma=np.sqrt(np.sum((Ds-bbmid)**2))/self.prevN

		if option=='bb':
			dyn=self.b*sigma
		elif option=='vd':
			slope=(Ds[-1]-Ds[0])/(self.prevN-1)
			appxLine=(np.array(range(self.prevN))*slope)+Ds[0] 
			dyn=np.sum(abs(appxLine-Ds))*(self.k/self.prevN)
		return dyn

	def calculate_twait(self, tmax, dyn):
		twait=int(np.ceil(tmax/(1+dyn*self.phi)))
		return twait

	def visualize(self, data, sampData, sampIdxes, visualizeLength=288*7):
		appxData=np.zeros(np.size(data))*np.nan

		sampIdxes=np.where(sampIdxes[:visualizeLength]==1)[0]
		for prevt, postt in zip(sampIdxes, sampIdxes[1:]):
			if postt-prevt==1:
				appxData[prevt]=sampData[prevt]
			else:
				slope=(sampData[postt]-sampData[prevt])/(postt-prevt-1)
				appxData[prevt:postt]=((np.array(range(prevt,postt))-prevt)*slope)+sampData[prevt]
			# 맨 마지막 data 채워야 함	
		
		fig=plt.figure(1)
		ax=plt.subplot(111)
		ax.set_xlabel('Time')
		ax.set_xticks([],[])

		ax.plot(data[:visualizeLength], 'b')
		ax.plot(appxData[:visualizeLength], 'r--')

		plt.show()

