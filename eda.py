
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style='darkgrid',color_codes=True)



## Raw data
# current_path=inspect.getfile(inspect.currentframe())
# current_dir=os.path.dirname(os.path.abspath(current_path))
airpi = pd.read_csv("Data/AirPiData.csv")
# print(airpi.head()) 

## Variable field
# columns: Data time, Volume [mV], Light_Level [Ohms], Temperature-DHT [Celsius], 
# Pressure [Hectopascal], Temperature-BMP [Celsius], Relative_Humidity [%], 
# Air_Quality [Ohms], Carbon_Monoxide [Ohms], Nitrogen_Dioxide [Ohms]



## Day time parsing
DatenTime=airpi['Date time'] # 2016-11-27 17:22:45 PM ~ 2017-07-30 12:05:30 PM (연속된 날이 아님)
dayLength={} # 길이가 288인 애들만 보면 될 듯. 
for i,x in enumerate(DatenTime):
	temp=x.split( )
	date=temp[0]
	time=temp[1]

	if date in dayLength.keys():
		dayLength[date][1]+=1
	else:
		dayLength[date]=[i, 1] # 이 date가 시작되는 index 저장, 날짜수를 count할 거니까 count 초기값은 1 

## 서로 다른 날짜의 수는 64일, 이 중 5분 간격 측정이 하루동안 온전하게 다 있는 일자의 수는 30
idxes=[dayLength[x][0] for x in dayLength if dayLength[x][1]==288] # 5분 측정이라, 하루 종일 측정 수 288개

## 범위를 크게 벗어나는 데이터 제외
i=0
while(i<len(idxes)):
	idx=idxes[i]

	temp_temp=airpi['Temperature-DHT [Celsius]'][idx:idx+288]
	temp_humi=airpi['Relative_Humidity [%]'][idx:idx+288]

	if temp_temp.between(0,100).all() or temp_humi.between(0,100).all(): # 범위를 일단 이렇게, left<=series<=right
		i+=1
	else: # 이상한 애가 섞여 있으면,
		print('remove', i)
		del idxes[i]



# Numpy array (TS에 주기가 잘 나타나는지 확인하기 위해 시각화를 해봄)
airq=np.array(airpi['Air_Quality [Ohms]'])
temp=np.array(airpi['Temperature-DHT [Celsius]']) # -960? ~ 41
humi=np.array(airpi['Relative_Humidity [%]']) # 17 ~ 1985? 



# New dataset (numpy), 아래 rough graph 3에서 새 데이터 만들고 저장.
nbDays=len(idxes)
save_airq=np.zeros((nbDays,288))
save_temp=np.zeros((nbDays,288))
save_humi=np.zeros((nbDays,288))


## Rough graph 1 (a single data, air quality)
# plt.plot(airq)

## Rough graph 2 (a day, air quality, temperature, humidity)#
#하루에 288번 측정 (5분마다)
# ㅑindex 80부터 2016-11-28 0:03 시작 --> [80:80+288] 하면 하루. (마지막 index는 80+288-1)
# lower=80 
# upper=80+288 # 14572 

# fig=plt.figure(1) # 1? 
# fig.suptitle('2016-11-28')

# ax=plt.subplot(311)
# ax.set_title('Air quality')
# ax.set_ylabel('[Ohms]')
# ax.set_xticks([], [])
# ax.plot(airq[lower:upper])

# ax=plt.subplot(312)
# ax.set_title('Temperature')
# ax.set_ylabel('[Celsius]')
# ax.set_xticks([], [])
# ax.plot(temp[lower:upper])

# ax=plt.subplot(313)
# ax.set_title('Relative humidity')
# ax.set_ylabel('[%]')
# ax.set_xticks([], [])
# ax.plot(humi[lower:upper])

# plt.show()

## Rough graph 3 (30 days, air quality, temperature, humidity)
lowers=idxes
uppers=[x+288 for x in idxes]

fig=plt.figure(1) # 1? 
fig.suptitle('30 days')

ax=plt.subplot(311)
ax.set_title('Air quality')
ax.set_ylabel('[Ohms]')
ax.set_xticks([], [])
for i in range(len(lowers)):
	data=airq[lowers[i]:uppers[i]]
	ax.plot(data)
	save_airq[i,:]=data

ax=plt.subplot(312)
ax.set_title('Temperature')
ax.set_ylabel('[Celsius]')
ax.set_xticks([], [])
for i in range(len(lowers)):
	data=temp[lowers[i]:uppers[i]]
	ax.plot(data)
	save_temp[i,:]=data

ax=plt.subplot(313)
ax.set_title('Relative humidity')
ax.set_ylabel('[%]')
ax.set_xticks([], [])
for i in range(len(lowers)):
	data=humi[lowers[i]:uppers[i]]
	ax.plot(data)
	save_humi[i,:]=data

plt.show()

# np.save('Data/ariq.npy', save_airq) # nbDays*288
# np.save('Data/temp.npy', save_temp) 
# np.save('Data/humi.npy', save_humi)

