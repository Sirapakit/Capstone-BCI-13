
file_name = "info_chb15_"

for i in range (10,17):
    f = open(file_name + str(i) + ".json" , "x")
    contents = "{\n    \"patient_ID\":\"chb15\",\n    \"raw_name\": \"chb15_.edf\",\n    \"channels\": {\n        \"number\": 38,\n        \"Fp2_F8\": 20,\n        \"F8_T8\": 21\n    },\n    \"time_stamp\" : {\n        \"start\": [],\n        \"end\": []\n    },\n    \"number_of_seizure\": \n}"
    f.write(contents)
    f.close()

#open and read the file after the appending:
# f = open("demofile3.txt", "r")
# print(f.read())