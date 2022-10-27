import json
  
data = open('./info.json')
f = json.load(data)

print(f['patient_ID'])
print("data_" + f['raw_name'].split('.')[0])
print(type(f['raw_name'].split('.')[0]))
print(256 * (f['time_stamp']['start'] - 30))
print(f['channels']["number"])
print((f['channels']["Fp2_F8"]) - 1)
print("../dataset/" + f["patient_ID"] + "/" + f["raw_name"])
print('../dataset/chb15/chb15_17.edf')
data.close()