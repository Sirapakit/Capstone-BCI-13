import json
  
data = open('./chb15/info_chb15_17.json')
f = json.load(data)

# print(f['patient_ID'])
# print("data_" + f['raw_name'].split('.')[0])
# print(type(f['raw_name'].split('.')[0]))
# print(256 * (f['time_stamp']['start'] - 30))
# print(f['channels']["number"])
# print((f['channels']["Fp2_F8"]) - 1)
# print("../dataset/" + f["patient_ID"] + "/" + f["raw_name"])
# print('../dataset/chb15/chb15_17.edf')

def box_text(text):
    lines = text.splitlines()
    width = max(len(s) for s in lines)
    res = [' '*7 + '#' + '─' * width + '#']
    for s in lines:
        res.append(' '*7 + '│' + (s + ' ' * width)[:width] + '│')
    res.append(' '*7 + '#' + '─' * width + '#')
    return '\n'.join(res)

number_of_seizure = f['number_of_seizure']
if (number_of_seizure == 0 ):
    print(box_text('NO SEIZURE DETECT'))
elif (number_of_seizure == 1):
    print(box_text('1 SEIZURE DETECT'))
elif (number_of_seizure >= 2):
    for i in range (number_of_seizure):
        print(box_text(f'{str(number_of_seizure).upper()} SEIZURE DETECT'))
else:
    print(box_text('ERROR: WRONG NUMBER_SEIZURE'))

print(f['time_stamp']['start'][0])

for i in range(2):
    print(f'Seizure NO {i}')
data.close()