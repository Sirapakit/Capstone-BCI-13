import json
  
data = open('./chb15/info_chb15_17.json')
f = json.load(data)



print(f['time_stamp']['start'][0])

for i in range(2):
    print(f'Seizure NO {i}')
data.close()