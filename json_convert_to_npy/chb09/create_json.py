
file_name = "info_chb09_"

for i in range (10,20):
    f = open(file_name + str(i) + ".json" , "x")
    contents = "{\n    \"patient_ID\":\"chb09\",\n    \"raw_name\": \"chb09_.edf\",\n    \"channels\": {\n        \"number\": 24,\n        \"Fp2_F8\": 13,\n        \"F8_T8\": 14\n    },\n    \"time_stamp\" : {\n        \"start\": [],\n        \"end\": []\n    },\n    \"number_of_seizure\": 0\n}"
    f.write(contents)
    f.close()

#open and read the file after the appending:
# f = open("demofile3.txt", "r")
# print(f.read())