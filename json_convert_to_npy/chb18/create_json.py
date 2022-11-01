
file_name = "info_chb18_"

for i in range (37):
    f = open(file_name + str(i) + ".json" , "x")
    contents = "{\n    \"patient_ID\":\"\",\n    \"raw_name\": \".edf\",\n    \"channels\": {\n        \"number\": ,\n        \"Fp2_F8\": ,\n        \"F8_T8\": \n    },\n    \"time_stamp\" : {\n        \"start\": [],\n        \"end\": []\n    },\n    \"number_of_seizure\": \n}"
    f.write(contents)
    f.close()

#open and read the file after the appending:
# f = open("demofile3.txt", "r")
# print(f.read())